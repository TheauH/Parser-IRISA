from config import transcription

maPage = transcription.Transcription("./test/Corpus_2021/Boudin-Torres-2006.pdf")[0]
maPage.découpe_page()
print(maPage)