from assets import username_exists, login_user, create_new_user, fetch_username, fetch_user_id, create_new_post, fetch_all_posts, valid_post_id, create_comment, fetch_post, fetch_post_comments
import time

main_loop = True
while main_loop:
    # SignUp and Login Options (Step-1)
    sign_up_login_loop = True
    while sign_up_login_loop:
        try:
            s1_option = int(input("\tSign-Up (1) | Log-In (2) | Quit App (3) => "))
            if s1_option == 1:
                sign_up_loop = True
                while sign_up_loop:
                    new_username = input("\tCreate a new Username => ")
                    if username_exists(new_username.lower().replace(" ", "")) == False:
                        valid_password_loop = True
                        while valid_password_loop:
                            choose_password = input("\tCreate a Strong Password (At Least 10 Characters) => ")
                            choose_password = choose_password.replace(" ", "")
                            if len(choose_password) < 10:
                                print("\tPassword Length Less than 10 Characters. Enter Again")
                                continue
                            valid_password_loop = False
                        ret = create_new_user(new_username, choose_password)
                        sign_up_loop = False
                        sign_up_login_loop = False
                    else:
                        print("\tUsername Already Exists. Enter Another Username")
                        continue
            elif s1_option == 2:
                login_loop = True
                while login_loop:
                    login_username = input("\tEnter Login-Username => ")
                    login_password = input("\tEnter Login-Password => ")
                    if login_user(login_username.lower().replace(" ", ""), login_password.replace(" ", "")) == True:
                        login_loop = False
                        sign_up_login_loop = False
                    else:
                        print("\tInvalid Login Credentials")
            elif s1_option == 3:
                print()
                print("\tThanks for using PrawnPost")
                print()
                sign_up_login_loop = False
            else:
                print("\tNo Such Option. ReEnter the Valid Option.")
        except:
            print("\tEnter Valid Input")
            continue

    # {Step-2} => Getting Post Log-In/Sign-Up Workflow User Details
    if s1_option == 1:
        current_username = new_username.lower().replace(" ", "")
        current_user_id = fetch_user_id(current_username)
        main_loop = False
    elif s1_option == 2:
        current_username = login_username.lower().replace(" ", "")
        current_user_id = fetch_user_id(current_username)
        main_loop = False
    elif s1_option == 3:
        main_loop = False
        exit()

user_state = lambda: "Log-In" if s1_option == 2 else "Sign-Up"
current_state = user_state()
print()
print(f"\t{current_state} Successful", "@"+current_username)
# print("\tYour User-ID is", current_user_id)
print()

# Post Sign-Up/Log-In CLI Application Workflow {Step-3}
print("\t\tWelcome @%s to PrawnPost CLI"%(current_username))
print()
app_loop = True
while app_loop:
    try:
        print()
        app_option = int(input("\tCreate New Post (1) | See Posts and Comment (2) | Quit App (3) => "))
        print()
        if app_option == 1:
            post_title_loop = True
            while post_title_loop:
                print()
                post_title = input("\tPost Title => ")
                print()
                if len(post_title.strip()) == 0:
                    print("\tPost Title Cannot Be Empty. Enter Again.")
                    continue
                else:
                    post_title_loop = False
            post_content_loop = True
            while  post_content_loop:
                print()
                post_content = input("\tPost Content => ")
                print()
                if len(post_content.strip()) == 0:
                    print("\tPost Content Cannot Be Empty. Enter Again.")
                    continue
                else:
                    post_content_loop = False
            # Creating the New Post
            create_new_post(current_user_id, post_title, post_content)
            print()
            print(f"\tNew Post Created by @{current_username}")
            print()
        elif app_option == 2:
            posts = fetch_all_posts()
            for post in posts:
                print()
                print("\tPost From => ", post[0])
                print("\tPost ID => ", post[1])
                print("\tPost Title => ", post[2])
                print("\tPost Content => ", post[3])
                print()
                time.sleep(1)
            # Comment Functions with No Replies and Nesting Starts Below
            comment_main_loop = True
            while comment_main_loop:
                try:
                    print()
                    comment_main_option = int(input("\tComment (1) | No Comment (2) | Read Comments (3) => "))
                    print()
                    if comment_main_option == 1:
                        post_loop = True
                        while post_loop:
                            print()
                            post_id = input("\tPost-ID you want to comment to => ")
                            post_id = post_id.replace(" ", "")
                            print()
                            if valid_post_id(post_id) == True:
                                comment_not_empty_loop = True
                                while comment_not_empty_loop:
                                    print()
                                    comment = input("\tEnter Your COMMENT => ")
                                    print()
                                    if len(comment.strip()) == 0:
                                        print()
                                        print("\tComment Cannot Be Empty. Write Comment Again.")
                                        print()
                                        continue
                                    comment_not_empty_loop = False
                                create_comment(current_user_id, post_id, comment)
                                print()
                                print("\tComment Successfully Made.")
                                print()
                                post_loop = False
                            else:
                                print()
                                print("\tInValid Post-ID. Enter Again.")
                                print()
                                continue
                    elif comment_main_option == 2:
                        comment_main_loop = False
                    elif comment_main_option == 3:
                        post_loop = True
                        while post_loop:
                            print()
                            post_id = input("\tPost-ID you want to Read Comments Of => ")
                            post_id = post_id.replace(" ", "")
                            print()
                            if valid_post_id(post_id) == True:
                                post = fetch_post(post_id)
                                print()
                                print("\tPost From => ", fetch_username(post[3]))
                                print("\tPost ID => ", post[0])
                                print("\tPost Title => ", post[1])
                                print("\tPost Content => ", post[2])
                                print()
                                post_comments = fetch_post_comments(post_id)
                                if len(post_comments) == 0:
                                    print()
                                    print("\tNo Comments Exist for this POST.")
                                    print()
                                else:
                                    print()
                                    print("\tDisplaying Comments ==>>")
                                    print()
                                    for comment in post_comments:
                                        print()
                                        print("\t\tComment From => ", fetch_username(comment[2]))
                                        print("\t\tComment Content => ", comment[1])
                                        print()
                                post_loop = False
                            else:
                                print()
                                print("\tInValid Post-ID. Enter Again.")
                                print()
                                continue
                    else:
                        print("\tNo Such Option. ReEnter.")
                except:
                    print()
                    print("\tInvalid Input. ReENTER.")
                    print()
                    continue
        elif app_option == 3:
            print()
            print("\tThanks for using PrawnPost")
            print()
            app_loop = False
        else:
            print()
            print("\tNo Such App Option")
            print()
    except:
        print()
        print("\tInvalid Option. Enter Again")
        print()

