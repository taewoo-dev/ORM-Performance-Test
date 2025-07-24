module default {
    type User {
        required property name -> str {
            constraint max_len_value(100);
        };
        required property email -> str {
            constraint exclusive;
            constraint max_len_value(255);
        };

        # Reverse link to posts
        multi link posts := .<user[is Post];
    }

    type Post {
        required property title -> str {
            constraint max_len_value(255);
        };
        required property content -> str;
        required link user -> User;
    }
} 