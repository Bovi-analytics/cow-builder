# $Id:
# Copyright:
"""
:module: DigitalHerd
:module author: Gabe van den Hoeven
    :synopsis: This module contains the DigitalHerd class representing a dairy herd.

======================
How To Use This Module
======================
(See the individual classes, methods, and attributes for details.)\n
This module is to be used in conjunction with the DigitalCow class.
The DigitalHerd contains certain variables used by the DigitalCow class for
simulation purposes. These variables are the same for all DigitalCow instances
in the herd.\n
Since default values are provided for the DigitalHerd class, it can be created as
follows:\n
1. Import the class DigitalHerd: \n
``import DigitalHerd.DigitalHerd`` or ``from DigitalHerd import DigitalHerd``.\n
2. Create a DigitalHerd instance. \n
``new_herd = DigitalHerd()``

"""


import numpy as np
import DigitalCow
from decimal import Decimal


class DigitalHerd:
    """
    A class to represent a digital herd of cows and manage their properties.

    Attributes:
        _mu_age_at_first_heat : int
            The mean age in days at which a cow
            will experience its first estrus.
        _sigma_age_at_first_heat : int
            The standard deviation in days of the age
            at which a cow will experience its first estrus.
        _voluntary_waiting_period : list[int]
            The voluntary waiting period in days before a
            cow can be inseminated.
        _milk_threshold : decimal.Decimal
            The minimum milk production in liters
            to be considered as a productive cow.
        _insemination_window : list[int]
            The number of days in milk since the voluntary waiting period after
            which a cow is no longer eligible for insemination.
        _herd : list[DigitalCow.DigitalCow]
            A list of DigitalCow objects representing the cows in the herd.
        _days_in_milk_limit : int
            The maximum number of days a cow can be in milk
            before being culled.
        _lactation_number_limit : int
            The maximum number of lactation cycles a cow can have
        before being culled.
        _days_pregnant_limit : list[int]
            The maximum number of days a cow can be pregnant.

    """
    def __init__(self, mu_age_at_first_heat=365, sigma_age_at_first_heat=0, vwp=None,
                 insemination_window=None, milk_threshold=Decimal("10"),
                 days_in_milk_limit=1000, lactation_number_limit=9,
                 days_pregnant_limit=None):
        """Initializes an instance of a DigitalHerd object.

        :param mu_age_at_first_heat: The mean age in days at which a cow
            will experience its first estrus.
        :type mu_age_at_first_heat: int
        :param sigma_age_at_first_heat: The standard deviation of the age
            at which a cow will experience its first estrus.
        :type sigma_age_at_first_heat: int
        :param vwp: The voluntary waiting period in days before a
            cow can be inseminated.
        :type vwp: list[int] | None
        :param insemination_window: The insemination window in days after
            which a cow is no longer eligible for insemination.
        :type insemination_window: list[int] | None
        :param milk_threshold: The minimum milk production in liters
            to be considered as a productive cow.
        :type milk_threshold: decimal.Decimal
        :param days_in_milk_limit: The maximum number of days a cow can be in milk
            before being culled.
        :type days_in_milk_limit: int
        :param lactation_number_limit: The maximum number of lactation cycles a cow
            can have before being culled.
        :type lactation_number_limit: int
        :param days_pregnant_limit: The maximum number of days a cow can be pregnant.
        :type days_pregnant_limit: list[int] | None
        """
        self._mu_age_at_first_heat = mu_age_at_first_heat
        self._sigma_age_at_first_heat = sigma_age_at_first_heat
        if vwp is None:
            self._voluntary_waiting_period = [365, 80, 60]
        else:
            self._voluntary_waiting_period = vwp
        self._milk_threshold = milk_threshold
        if insemination_window is None:
            self._insemination_window = [100, 100, 100]
        else:
            self._insemination_window = insemination_window
        self._insemination_window = insemination_window
        self._herd = []
        self._days_in_milk_limit = days_in_milk_limit
        self._lactation_number_limit = lactation_number_limit
        if days_pregnant_limit is None:
            self._days_pregnant_limit = [279, 280, 282]
        else:
            self._days_pregnant_limit = days_pregnant_limit
        # other general properties shared between the entities in the _herd

    def add_to_herd(self, cows=list) -> None:
        """
        Takes a list of DigitalCow objects and adds each cow to the herd if they
        are not in the herd already.

        :param cows: A list of DigitalCow objects which are to be added to the herd.
        :type cows: list[DigitalCow.DigitalCow]
        :raises TypeError: If the list given does not solely consist of DigitalCow
            objects.
        """
        if cows is not None:
            for cow in cows:
                if isinstance(cow, DigitalCow.DigitalCow):
                    if cow not in self.herd:
                        self.herd.append(cow)
                        cow.herd = self
                else:
                    raise TypeError("The given list should only contain DigitalCow "
                                    "objects.")

    def calculate_mu_age_at_first_heat(self):
        """
        Calculates the mean age in days at which a cow in the herd will experience
        its first estrus.
        """
        mu_age_at_first_heat = 0
        for cow in self.herd:
            if cow.age_at_first_heat is not None:
                mu_age_at_first_heat += cow.age_at_first_heat
        mu_age_at_first_heat = mu_age_at_first_heat / len(self.herd)
        if not mu_age_at_first_heat == 0:
            self.mu_age_at_first_heat = mu_age_at_first_heat

    def generate_age_at_first_heat(self) -> int:
        """
        Returns a random age at first heat based on the mean age at first heat
        and its standard deviation.
            :returns: A random age at first heat based on the mean age at first heat
                and its standard deviation.
            :rtype: int
        """
        self.calculate_mu_age_at_first_heat()
        return np.random.normal(self.mu_age_at_first_heat,
                                self.sigma_age_at_first_heat)

    @property
    def mu_age_at_first_heat(self):
        return self._mu_age_at_first_heat

    @mu_age_at_first_heat.setter
    def mu_age_at_first_heat(self, mu):
        self._mu_age_at_first_heat = mu

    @property
    def sigma_age_at_first_heat(self):
        return self._sigma_age_at_first_heat

    @sigma_age_at_first_heat.setter
    def sigma_age_at_first_heat(self, sigma):
        self._sigma_age_at_first_heat = sigma

    @property
    def herd(self) -> list:
        return self._herd

    @herd.setter
    def herd(self, herd):
        all_instances = True
        if type(herd) == list:
            for cow in herd:
                if not isinstance(cow, DigitalCow.DigitalCow):
                    all_instances = False
            if all_instances:
                self._herd = herd
                for cow in self._herd:
                    cow.herd = self
            else:
                raise TypeError(
                    "Herd property has to be a list of DigitalCow objects")

    def get_voluntary_waiting_period(self, lactation_number) -> int:
        if lactation_number > 2:
            lactation_number = 2
        return self._voluntary_waiting_period[lactation_number]

    def set_voluntary_waiting_period(self, vwp):
        for i in vwp:
            if not type(i) == int:
                raise TypeError
        self._voluntary_waiting_period = vwp

    @property
    def milk_threshold(self) -> Decimal:
        return self._milk_threshold

    @milk_threshold.setter
    def milk_threshold(self, mt):
        if type(mt) == Decimal:
            self._milk_threshold = mt

    def get_insemination_window(self, lactation_number) -> int:
        if lactation_number > 2:
            lactation_number = 2
        return self._insemination_window[lactation_number]

    def set_insemination_window(self, dim_window):
        for i in dim_window:
            if not type(i) == int:
                raise TypeError
        self._insemination_window = dim_window

    @property
    def days_in_milk_limit(self) -> int:
        return self._days_in_milk_limit

    @days_in_milk_limit.setter
    def days_in_milk_limit(self, limit):
        self._days_in_milk_limit = limit

    @property
    def lactation_number_limit(self) -> int:
        return self._lactation_number_limit

    @lactation_number_limit.setter
    def lactation_number_limit(self, limit):
        self._lactation_number_limit = limit

    def get_days_pregnant_limit(self, lactation_number) -> int:
        if lactation_number > 2:
            lactation_number = 2
        return self._days_pregnant_limit[lactation_number]

    def set_days_pregnant_limit(self, limit):
        for i in limit:
            if not type(i) == int:
                raise TypeError
        self._days_pregnant_limit = limit
