import os

# path of the Windows host file
host_path = r"C:\Windows\System32\Drivers\etc\hosts"
# localhost IP address      
redirect = "127.0.0.1"

website = None
website_list = []

with open(host_path, "a+") as file:

    # apply each line in the file to a list
    file.seek(0)
    info = file.readlines()

    # check for blocked websites and add them to website_list
    for line in info:
        if redirect == line.split()[0]:
            website_list.append(line.split()[1])

    while True:
        print("Type 'del' to delete a website from blocked list."
              "\nType 'exit' to close the program.")

        # website = str(input("Enter the websites you want to block: "))
        website = "del"

        if website == "exit" or website == "del":
            break
        elif website == "ls":
            print("\nList of blocked websites:", website_list)
            for website in website_list:
                print(website)
        else:
            # add onto the blocked list if website not on there
            if website not in website_list:
                website_list.append(website)

                if len(info) > 1:
                    if "\n" not in info[-1]:
                        file.write("\n")

                # add localhost IP address with the website next to it
                file.write(redirect + " " + website + "\n")
                # flush it onto the file to immediately take in effect
                file.flush()
                os.fsync(file.fileno())

        print()

if website == "del":
    with open(host_path, "r+") as file:

        while True:
            # get all the lines of the file
            info = file.readlines()
            # adjust file pointer to the beginning
            file.seek(0)

            flag = False

            delWebsite = str(input("Enter a website to delete: "))

            if delWebsite == "exit":
                break

            if delWebsite not in website_list:
                print("Website not found.")
            else:
                if len(website_list) == 1:
                    if delWebsite in website_list:
                        website_list.remove(delWebsite)
                        file.truncate(0)
                elif len(website_list) == 0:
                    print("There are no blocked websites.")
                    break
                else:
                    for line in info:
                        # write all the lines back if current line doesn't contain website to be unblocked
                        if delWebsite not in line:
                            flag = True
                            file.write(line)
                            file.flush()
                            os.fsync(file.fileno())
                        # update the blocked website list
                        # elif delWebsite in line:
                        #     print("b")
                        #     website_list.remove(delWebsite)
                        # delete the rest of the file after the file pointer and update file immediately
                    if flag == True:
                        file.truncate()
                        file.flush()
                        os.fsync(file.fileno())
