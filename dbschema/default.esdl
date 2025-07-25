module default {
    type User {
        required name -> str {
            constraint max_len_value(100);
        };
        required email -> str {
            constraint exclusive; # unique
            constraint max_len_value(255);
        };

        # Reverse link to posts
        multi link posts := .<user[is Post];
    }

    type Post {
        required title -> str {
            constraint max_len_value(255);
        };
        required content -> str;
        required link user -> User;
    }
}