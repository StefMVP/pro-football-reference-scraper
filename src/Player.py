class Player:
    Name = ''
    Position = ''
    UrlStub = ''
    Team = ''

    def __init__(self, nameParam, positionParam, urlStubParam, teamParam):
        self.Name = nameParam.strip() if nameParam else ''
        self.Position = positionParam.strip() if positionParam else ''
        self. UrlStub = urlStubParam.strip() if urlStubParam else ''
        self.Team = teamParam.strip() if teamParam else ''

