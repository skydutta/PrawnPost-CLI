from assets import username_exists, login_user, create_new_user, fetch_user_id, create_new_post

main_loop = True
while main_loop:
    # SignUp and Login Options (Step-1)
    sign_up_login_loop = True
    while sign_up_login_loop:
        try:
            s1_option = int(input("\tSign-Up (1) and Log-In (2) => "))
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
    print()
    app_option = int(input("\tCreate New Post (1) | See Posts and Comment (2) => "))
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
        pass
    else:
        print()
        print("\tNo Such App Option")
        print()

