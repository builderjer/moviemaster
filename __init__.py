from mycroft import MycroftSkill, intent_file_handler


class Tmdb(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('tmdb.intent')
    def handle_tmdb(self, message):
        self.speak_dialog('tmdb')


def create_skill():
    return Tmdb()

