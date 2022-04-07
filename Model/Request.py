from Model.tools import *


class Request:
    def __init__(
            self, request_number, request_name=None, request_status=None, request_father=None, request_type=None,
            request_business_line=None, request_business=None, request_app=None, request_dev_area=None,
            request_dev_factory=None, request_interested=None, request_summary=None, request_teams=None
    ):
        self.__app = request_app.lower()
        self.__business = request_business.lower()

        # normalizando `business_line`
        self.__business_line = str()
        if request_business_line.lower() in globals()['BUSINESS_LINE']:
            self.__business_line = globals()['BUSINESS_LINE'][request_business_line.lower()]

        self.__interested = set()
        if isinstance(request_interested, set):
            self.__interested = request_interested
        elif isinstance(request_interested, str):
            self.append_interested(request_interested)

        self.__dev_area = request_dev_area.lower()

        # normalizando `dev_factory`
        self.__dev_factory = str()
        if request_dev_factory.lower() in globals()['DEV_FACTORY']:
            self.__dev_factory = globals()['DEV_FACTORY'][request_dev_factory.lower()]

        self.__father = request_father
        self.__name = normalize_str(request_name)
        self.__number = request_number
        self.__status = request_status
        self.__summary = request_summary

        self.__teams = set()
        if isinstance(request_teams, set):
            self.__teams = request_teams
        elif isinstance(request_teams, str):
            self.__teams = set((request_teams,))
        else:
            self.make_teams()

        self.__type = prefix(request_type)

    @property
    def app(self) -> str:
        return self.__app

    @app.setter
    def app(self, request_app: str) -> None:
        self.__app = request_app

    @property
    def business(self) -> str:
        return self.__business

    @business.setter
    def business(self, request_business: str) -> None:
        self.__business = request_business

    @property
    def business_line(self) -> str:
        return self.__business_line

    @business_line.setter
    def business_line(self, request_business_line: str) -> None:
        self.__business_line = request_business_line

    @property
    def interested(self) -> set:
        return self.__interested

    @interested.setter
    def interested(self, request_interested: set) -> None:
        self.__interested = request_interested

    def append_interested(self, *args):
        self.__interested.update(args)

    @property
    def dev_area(self) -> str:
        return self.__dev_area

    @dev_area.setter
    def dev_area(self, request_dev_area: str) -> None:
        self.__dev_area = request_dev_area

    @property
    def dev_factory(self) -> str:
        return self.__dev_factory

    @dev_factory.setter
    def dev_factory(self, request_dev_factory: str) -> None:
        self.__dev_factory = request_dev_factory

    @property
    def father(self) -> str:
        return self.__father

    @father.setter
    def father(self, request_father: str) -> None:
        self.__father = request_father

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, request_name: str) -> None:
        self.__name = normalize_str(request_name)

    @property
    def number(self) -> str:
        return self.__number

    @number.setter
    def number(self, request_number: str) -> None:
        self.__number = request_number

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, request_status: str) -> None:
        self.__status = request_status

    @property
    def summary(self) -> str:
        return self.__summary

    @summary.setter
    def summary(self, request_summary: str) -> None:
        self.__summary = request_summary

    @property
    def teams(self) -> set:
        return self.__teams

    @teams.setter
    def teams(self, request_teams: set) -> None:
        self.__teams = request_teams

    def append_teams(self, *args) -> None:
        self.__teams.update(args)

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, request_type: str) -> None:
        self.__type = request_type

    def make_teams(self):
        """
        Completa el conjunto de los equipos.
        `bl` variable auxiliar para `self.__business_line`.
        `df` variable auxiliar para `self.__dev_factory`.
        `teams` variable auxiliar para contener los equipos.
        `ap` variable auxiliar para `self.__app`.
        `da` variable auxiliar para ``
        :return:
        """

        # normalizando `teams`
        teams = set()
        if self.__dev_factory in globals()['DEV_TEAMS']:
            if is_dict(globals()['DEV_TEAMS'][self.__dev_factory]):
                teams.add(globals()['DEV_TEAMS'][self.__dev_factory][self.__business_line])
            else:
                teams.add(globals()['DEV_TEAMS'][self.__dev_factory])

        if self.__business_line in globals()['QA_TEAMS']:
            teams.add(globals()['QA_TEAMS'][self.__business_line])

        # ap = self.__app.lower()
        if self.__app in globals()['APP_TEAMS']:
            teams.add(globals()['APP_TEAMS'][self.__app])

        # da = self.__dev_area.lower()
        if self.__dev_area in globals()['DEV_AREA']:
            teams.add(globals()['DEV_AREA'][self.__dev_area])

        return teams

    def __str__(self):
        return 'Request {' + f'''
    "app": "{self.app}",
    "business": "{self.business}",
    "business_line": "{self.business_line}",
    "interested": "{self.interested}",
    "dev_area": "{self.dev_area}",
    "dev_factory": "{self.dev_factory}",
    "father": "{self.father}",
    "name": "{self.name}",
    "number": "{self.number}",
    "status": "{self.status}",
    "summary": "{self.summary}"
    "type": "{self.type}"
''' + '}'


class TestPlan:
    def __init__(self, number, name, summary):
        self.number = number
        self.name = name
        self.summary = summary

    def __str__(self):
        return f'TestPlan<Name: {self.name}>'


class MantisProject:
    def __init__(self, number, name, summary):
        pass


if __name__ == '__main__':
    print(globals()['APP_TEAMS']['sap'])
