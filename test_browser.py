from skills.browser import BrowserSkill

browser = BrowserSkill()

while True:

    print("\n1. YouTube")
    print("2. GitHub")
    print("3. Gmail")
    print("4. ChatGPT")
    print("5. Google Search")
    print("6. YouTube Search")
    print("0. Exit")

    choice = input("\nChoice : ")

    if choice == "0":
        break

    elif choice == "1":
        browser.youtube()

    elif choice == "2":
        browser.github()

    elif choice == "3":
        browser.gmail()

    elif choice == "4":
        browser.chatgpt()

    elif choice == "5":

        q = input("Search : ")

        browser.google_search(q)

    elif choice == "6":

        q = input("YouTube Search : ")

        browser.youtube_search(q)
        