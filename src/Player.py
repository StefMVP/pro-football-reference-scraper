class Player:
    Name = ''
    Position = ''
    UrlStub = ''

    def __init__(self, nameParam, positionParam, urlStubParam):
        self.Name = nameParam.strip() if nameParam else ''
        self.Position = positionParam.strip() if positionParam else ''
        self. UrlStub = urlStubParam.strip() if urlStubParam else ''

