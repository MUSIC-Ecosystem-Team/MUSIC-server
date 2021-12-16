import mutagen


class MusicFileHandler:
    def __init__(self, filePath):
        self.musicFile = mutagen.File(filePath)
        self.fileType = ""
        if isinstance(self.musicFile, type(None)):
            #print("file: no tags found")
            pass
        elif isinstance(self.musicFile, mutagen.mp3.MP3):
            #print("file: mp3")
            self.fileType = "mp3"
        elif isinstance(self.musicFile, mutagen.flac.FLAC):
            #return Response(xml, mimetype='text/xml')print("file: flac")
            self.fileType = "flac"
    
    def OK(self):
        return self.fileType != ""

    def getTags(self):
        """ Switch to get tags from the file """
        if self.fileType == "mp3":
            return self.getMp3Tags()
        elif self.fileType == "flac":
            return self.getFlacTags()
        else:
            return None

    def getMp3Tags(self):
        tags = {}
        for tag in self.musicFile.tags:

            if isinstance(self.musicFile.tags[tag], mutagen.id3.TALB):
                tags["album"] = self.musicFile.tags[tag].text[0]
            elif isinstance(self.musicFile.tags[tag], mutagen.id3.TPE1):
                tags["albumartist"] = self.musicFile.tags[tag].text[0]
            elif isinstance(self.musicFile.tags[tag], mutagen.id3.TPE2):
                tags["artist"] = self.musicFile.tags[tag].text[0]
            elif isinstance(self.musicFile.tags[tag], mutagen.id3.TRCK):
                tags["tracknumber"] = self.musicFile.tags[tag].text[0]
            elif isinstance(self.musicFile.tags[tag], mutagen.id3.TPOS):
                tags["discnumber"] = self.musicFile.tags[tag].text[0]
            elif isinstance(self.musicFile.tags[tag], mutagen.id3.TCON):
                tags["genre"] = self.musicFile.tags[tag].text[0]
            elif isinstance(self.musicFile.tags[tag], mutagen.id3.TDRC):
                tags["date"] = str(self.musicFile.tags[tag].text[0])
            
        return tags

    def getFlacTags(self):
        tags = {}
        for tag in self.musicFile.tags:
            tags[tag[0]] = tag[1]
        return tags



""" with open("cover", "wb") as cover:
    #cover.write(musicTags.get("APIC:").data)
    print(musicTags.get("APIC:").mime) """


# [('artist', 'Von Kaiser'), ('title', 'Wavelengths'), ('isrc', 'QZAMM1800206'), ('tracknumber', '2'), ('discnumber', '1'), ('tracktotal', '13'), ('disctotal', '1'), ('album', 'Ghosts of Miami'), ('genre', 'New Wave; Retrowave; Synthpop; Synthwave'), ('date', '2020'), ('label', 'Von Kaiser Music'), ('albumartist', 'Von Kaiser'), ('upc', '193339260365')]

# {'TIT2': TIT2(encoding=<Encoding.UTF16: 1>, text=["Hangin' On You"]), 'TPE1': TPE1(encoding=<Encoding.UTF16: 1>, text=['Nena']), 'TPE2': TPE2(encoding=<Encoding.UTF16: 1>, text=['Nena']), 'TALB': TALB(encoding=<Encoding.UTF16: 1>, text=['99 Luftballons']), 'TRCK': TRCK(encoding=<Encoding.UTF16: 1>, text=['3/0']), 'TPOS': TPOS(encoding=<Encoding.UTF16: 1>, text=['1/0']), 'TCON': TCON(encoding=<Encoding.UTF16: 1>, text=['Pop']), 'APIC:': APIC(encoding=<Encoding.LATIN1: 0>, mime='image/jpeg', type=<PictureType.COVER_FRONT: 3>, desc='', data=b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x0

""" <class 'mutagen.id3.TPE2'> ['Nena']
<class 'mutagen.id3.TALB'> ['99 Luftballons']
<class 'mutagen.id3.TRCK'> ['4/0']
<class 'mutagen.id3.TPOS'> ['1/0']
<class 'mutagen.id3.TCON'> ['Pop'] """