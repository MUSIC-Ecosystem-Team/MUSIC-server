import mutagen


class MusicFileHandler:
    def __init__(self, filePath):
        self.fileType = ""
        try:
            self.musicFile = mutagen.File(filePath)
            if isinstance(self.musicFile, type(None)):
                #print("file: no tags found")
                pass
            elif isinstance(self.musicFile, mutagen.mp3.MP3):
                #print("file: mp3")
                self.fileType = "mp3"
            elif isinstance(self.musicFile, mutagen.flac.FLAC):
                #return Response(xml, mimetype='text/xml')print("file: flac")
                self.fileType = "flac"
        except:
            pass
    
    def OK(self):
        return self.fileType != ""

    def getPicture(self):
        """ Switch to get picture from the file """
        if self.fileType == "mp3":
            for tag in self.musicFile.tags:
                if isinstance(self.musicFile.tags[tag], mutagen.id3.APIC):
                    return self.musicFile.tags[tag].mime, self.musicFile.tags[tag].data
        elif self.fileType == "flac":
            return None, None

        return None, None

    def getTags(self):
        """ Switch to get tags from the file """
        if self.fileType == "mp3":
            return self.getMp3Tags()
        elif self.fileType == "flac":
            return self.getFlacTags()
        else:
            return None

    def getMp3Tags(self):
        tags = {"title": "", "artist": "", "albumartist": "", "album": "", "title": "", "tracknumber": "", "tracktotal": "", "discnumber": "", "disctotal": "", "date": "", "genre": ""}
        for tag in self.musicFile.tags:

            if isinstance(self.musicFile.tags[tag], mutagen.id3.TOAL):
                tags["title"] = self.musicFile.tags[tag].text[0]
            elif isinstance(self.musicFile.tags[tag], mutagen.id3.TIT2):
                tags["title"] = self.musicFile.tags[tag].text[0]
            elif isinstance(self.musicFile.tags[tag], mutagen.id3.TALB):
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
        tags = {"title": "", "artist": "", "albumartist": "", "album": "", "title": "", "tracknumber": "", "tracktotal": "", "discnumber": "", "disctotal": "", "date": "", "genre": ""}
        for tag in self.musicFile.tags:
            tags[tag[0].lower()] = tag[1]
        return tags

