from locust import HttpUser, task, between
import random
import string
import json
import uuid

class ORMPerformanceTest(HttpUser):
    """
    ORM 성능 테스트를 위한 Locust 사용자 클래스
    각 ORM (SQLAlchemy, Tortoise, EdgeDB)에 대해 동일한 패턴으로 테스트
    """
    wait_time = between(1, 3)  # 1-3초 대기
    
    def on_start(self):
        """테스트 시작 시 초기 설정"""
        self.created_users = []
        self.created_posts = []
        self.orm_type = self.detect_orm_type()
        
    def detect_orm_type(self):
        """현재 테스트 중인 ORM 타입 감지"""
        try:
            response = self.client.get("/health")
            if response.status_code == 200:
                return response.json().get("orm", "unknown")
        except:
            pass
        return "unknown"
    
    def generate_random_string(self, length=10):
        """랜덤 문자열 생성"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def generate_email(self):
        """랜덤 이메일 생성"""
        return f"user_{self.generate_random_string(8)}@test.com"

    @task(3)  # 가중치 3: 사용자 생성이 자주 호출됨
    def create_user(self):
        """사용자 생성 테스트"""
        user_data = {
            "name": f"User {self.generate_random_string(5)}",
            "email": self.generate_email()
        }
        
        with self.client.post("/users", json=user_data, catch_response=True) as response:
            if response.status_code == 201 or response.status_code == 200:
                user = response.json()
                self.created_users.append(user)
                response.success()
            elif response.status_code == 400 and "Email already exists" in response.text:
                # 이메일 중복은 허용 가능한 에러
                response.success()
            else:
                response.failure(f"Failed to create user: {response.status_code}")

    @task(5)  # 가중치 5: 사용자 목록 조회가 가장 자주 호출됨
    def get_users(self):
        """사용자 목록 조회 테스트 (페이징)"""
        skip = random.randint(0, 10)
        limit = random.randint(5, 20)
        
        with self.client.get(f"/users?skip={skip}&limit={limit}", catch_response=True) as response:
            if response.status_code == 200:
                users = response.json()
                response.success()
            else:
                response.failure(f"Failed to get users: {response.status_code}")

    @task(4)  # 가중치 4: 특정 사용자 조회
    def get_user_by_id(self):
        """특정 사용자 조회 테스트"""
        if not self.created_users:
            return
        
        user = random.choice(self.created_users)
        user_id = user["id"]
        
        with self.client.get(f"/users/{user_id}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # 사용자가 없을 수 있음 (다른 워커에서 생성된 경우)
                response.success()
            else:
                response.failure(f"Failed to get user: {response.status_code}")

    @task(2)  # 가중치 2: 게시글 생성
    def create_post(self):
        """게시글 생성 테스트"""
        if not self.created_users:
            # 사용자가 없으면 임시로 생성
            self.create_user()
            return
        
        user = random.choice(self.created_users)
        post_data = {
            "title": f"Post {self.generate_random_string(8)}",
            "content": f"This is test content {self.generate_random_string(20)}",
            "user_id": user["id"]
        }
        
        with self.client.post("/posts", json=post_data, catch_response=True) as response:
            if response.status_code == 201 or response.status_code == 200:
                post = response.json()
                self.created_posts.append(post)
                response.success()
            elif response.status_code == 404 and "User not found" in response.text:
                # 해당 사용자가 삭제되었을 수 있음
                response.success()
            else:
                response.failure(f"Failed to create post: {response.status_code}")

    @task(4)  # 가중치 4: 게시글 목록 조회
    def get_posts(self):
        """게시글 목록 조회 테스트 (페이징)"""
        skip = random.randint(0, 10)
        limit = random.randint(5, 15)
        
        with self.client.get(f"/posts?skip={skip}&limit={limit}", catch_response=True) as response:
            if response.status_code == 200:
                posts = response.json()
                response.success()
            else:
                response.failure(f"Failed to get posts: {response.status_code}")

    @task(3)  # 가중치 3: 사용자별 게시글 조회
    def get_user_posts(self):
        """사용자별 게시글 조회 테스트"""
        if not self.created_users:
            return
        
        user = random.choice(self.created_users)
        user_id = user["id"]
        skip = random.randint(0, 5)
        limit = random.randint(5, 10)
        
        with self.client.get(f"/users/{user_id}/posts?skip={skip}&limit={limit}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # 사용자가 없을 수 있음
                response.success()
            else:
                response.failure(f"Failed to get user posts: {response.status_code}")

    @task(1)  # 가중치 1: 성능 벤치마크 (가끔만 실행)
    def benchmark_orm_performance(self):
        """ORM별 성능 벤치마크 테스트"""
        if self.orm_type == "sqlalchemy_v2":
            endpoint = "/benchmark/sync-to-async"
        elif self.orm_type == "tortoise":
            endpoint = "/benchmark/native-async"
        elif self.orm_type == "edgedb":
            endpoint = "/benchmark/edgedb-native"
        else:
            return
        
        with self.client.get(endpoint, catch_response=True) as response:
            if response.status_code == 200:
                benchmark_data = response.json()
                # 벤치마크 결과를 로그에 출력
                print(f"\n=== {self.orm_type.upper()} Benchmark Results ===")
                if "average_conversion_time" in benchmark_data:
                    print(f"Average Conversion Time: {benchmark_data['average_conversion_time']:.4f}s")
                    print(f"Conversions per Second: {benchmark_data['conversions_per_second']:.2f}")
                elif "average_query_time" in benchmark_data:
                    print(f"Average Query Time: {benchmark_data['average_query_time']:.4f}s")
                    print(f"Queries per Second: {benchmark_data['queries_per_second']:.2f}")
                print("=" * 40)
                response.success()
            else:
                response.failure(f"Failed to run benchmark: {response.status_code}")


class SQLAlchemyUser(ORMPerformanceTest):
    """SQLAlchemy 전용 사용자 클래스"""
    host = "http://localhost:8001"


class TortoiseUser(ORMPerformanceTest):
    """Tortoise ORM 전용 사용자 클래스"""
    host = "http://localhost:8002"


class EdgeDBUser(ORMPerformanceTest):
    """EdgeDB 전용 사용자 클래스"""
    host = "http://localhost:8003" 