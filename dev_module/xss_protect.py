
class xxs_protect():
    @staticmethod
    def stop_code_filter(target):
        target = target.replace('<', '&lt;').replace('>', '&gt;').replace('\r\n', '<br>')
        return target