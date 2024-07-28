from .agents import youtube_transcriber

def main():
    """Main function"""
    while True:
        query = input("YouTube 📺:")

        youtube_transcriber.chat(query) 


if __name__ == "__main__":
    main()

