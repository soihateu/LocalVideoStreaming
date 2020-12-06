import Streamer
import StreamViewer

class login:
    print()
    print("Welcome to StreamBot, please enter your username followed by your password")
    print()
    username = input("Username: ")
    password = input("Password: ")
    print()
    u = open("usernames.txt", "r")
    p = open("passwords.txt", "r")
        
    c1 = 1
    c2 = 1
    i=0

    for line in u:
        if username == line.strip():
            uc = c1
            for line in p:
                if password == line.strip():
                    pc = c2
                    break
                c2=c2+1
        else:
            c1=c1+1
            continue
        break

    u.close()
    p.close()
        
    if c1!=c2:
        print("Access DENIED")
        exit()

    print("Access Granted!")
    print()
    print("Welcome " + username + "! Would you like to start a stream or join a stream?")
    print()

    while i==0:
        choice = input("1 to start streaming, 2 to join stream: ")
        if choice == "1":
            i=1
            try:
                Streamer.main()
            except:
                print("Error: Someone else is streaming")
        elif choice == "2":
            i=1
            server = input("Please enter server name/address: ")
            StreamViewer.main(server, username)
        else:
            print("Invalid option, please enter 1 to start stream or 2 to join a stream")
