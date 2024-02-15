from mutagen.id3 import ID3, APIC
from pathlib import Path
from PIL import Image
from io import BytesIO


class AddAlbumCover:
    def __init__(self, path) -> None:
        self.path = Path(path)
        self.audio = ID3(self.path)

    def add_art(self, img):
        img = Path(img)
        with open(img, "rb") as f:
            image_data = f.read()

        if img.suffix == ".jpg":
            mime_type = "image/jpg"
        elif img.suffix == ".png":
            mime_type = "image/png"
        else:
            print(f"wrong image type: {img.suffix}")
            return
        image = APIC(
            encoding=3,
            mime=mime_type,
            type=2,
            desc=img.name,
            data=image_data,
        )
        self.audio.delall("APIC")
        self.audio.add(image)
      
        self.audio.save()

    def show_art(self):
        for k, v in self.audio.items():
            if "APIC" in k:
                image = Image.open(BytesIO(v.data))
                image.show()
                return
        else:
            print("No embedded cover art found.")


#if __name__ == "__main__":
#    mp3_file_path = r"C:\Users\denni\Downloads\Leave Before You Love Me.mp3"
#    audio = AddAlbumCover(mp3_file_path)
#    audio.add_art(r"C:\python\Youtube-Downloader\Main\thumbnail.jpg")
#    audio.show_art()