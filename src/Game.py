class Game:
    Date = ''
    StartTime = ''
    Stadium = ''
    TimeOfGame = ''
    Attendance = ''
    Roof = ''
    Surface = ''
    Temperature = ''
    RelativeHumidity = ''
    WindMph = ''

    def __init__(self, DateParam, StartTimeParam, StadiumParam, TimeOfGameParam, AttendanceParam, RoofParam, SurfaceParam, TemperatureParam, RelativeHumidityParam, WindMphParam):
        self.Date = DateParam
        self.StartTime = StartTimeParam
        self.Stadium = StadiumParam
        self.TimeOfGame = TimeOfGameParam
        self.Attendance = AttendanceParam
        self.Roof = RoofParam
        self.Surface = SurfaceParam
        self. Temperature = TemperatureParam
        self. RelativeHumidity = RelativeHumidityParam
        self. WindMph = WindMphParam
