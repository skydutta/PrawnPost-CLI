from assets import username_exists, login_user, create_new_user, fetch_user_id

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

    # {Step-2} => Post Log-In/Sign-Up Workflow
    if s1_option == 1:
        current_username = new_username.lower().replace(" ", "")
        current_user_id = fetch_user_id(current_username)
        print("\tSign-Up Successful", current_username)
        print("\tYour User-ID is", current_user_id)
        main_loop = False
    elif s1_option == 2:
        current_username = login_username.lower().replace(" ", "")
        current_user_id = fetch_user_id(current_username)
        print("\tLog-In Successful", current_username)
        print("\tYour User-ID is", current_user_id)
        main_loop = False