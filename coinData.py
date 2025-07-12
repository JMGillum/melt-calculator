import weights
import metals


class CoinData:
    def __init__(
        self,
        weight: float | int | weights.Weight = None,
        metal=None,
        fineness=None,
        precious_metal_weight=None,
        years=None,
        country=None,
        denomination=None,
        nickname=None,
        value = None,
        retention = None
    ):
        if isinstance(weight, float) or isinstance(weight, int):
            self.weight = weights.Weight(weight, weights.Units.GRAMS)
        else:
            self.weight = weight
        self.metal = metal
        self.fineness = fineness
        self.precious_metal_weight = precious_metal_weight
        self.years = years
        self.country = country
        self.denomination = denomination
        self.nickname = nickname
        if (
            precious_metal_weight is None
            and weight is not None
            and fineness is not None
        ):
            self.precious_metal_weight = weights.Weight(
                round(self.weight.as_troy_ounces() * self.fineness, 4),
                weights.Units.TROY_OUNCES,
            )
        self.value = value
        if retention is None: # Percentage of melt value that coin is typically bought at
            self.default_retention = True
            self.retention = 1.00
        else:
            self.default_retention = False
            self.retention = retention 

    def yearsList(self):
        if self.years is not None:
            if isinstance(self.years, int):
                return str(self.years)
            if (
                isinstance(self.years, list)
                and len(self.years) > 0
                and isinstance(self.years[0], int)
            ):
                string = ""
                start_year = None
                previous_year = None
                for i in range(len(self.years)):
                    year = self.years[i]
                    if start_year is None:
                        start_year = year
                    if previous_year is not None and ((year - previous_year) > 1):
                        string += f"{start_year}"
                        if not start_year == previous_year:
                            string += f"-{previous_year}"
                        string += ","
                        start_year = year
                        previous_year = None
                    if i >= (len(self.years) - 1):
                        if previous_year is not None:
                            string += f"{start_year}-{year}"
                            start_year = year
                        else:
                            string += f"{year}"
                    previous_year = year

                return string
        return "Unknown years"

    def metalString(self):
        if self.metal is not None:
            if self.metal == metals.Metals.GOLD:
                return "Gold"
            elif self.metal == metals.Metals.SILVER:
                return "Silver"
        return "Unknown metal"
    
    def price(self,silver_price,gold_price):
        if self.metal is not None and self.weight is not None:
            if self.metal == metals.Metals.GOLD:
                self.value = self.precious_metal_weight.as_troy_ounces() * gold_price
            elif self.metal == metals.Metals.SILVER:
                self.value = self.precious_metal_weight.as_troy_ounces() * silver_price
        

    def asAString(self, format: str):
        """Very simple attempt at a format string for information
        %c - country
        %d - denomination
        %y - years
        %a - actual precious metal weight
        %m - metal
        %f - fineness
        %F - fineness as a percent (fineness*100)
        %w - weight
        %n - nickname
        %v - value
        %V - Price retention value (value * retention percentage)
        """
        string = format
        string = string.replace(
            "%c", "Unknown country" if self.country is None else self.country.title()
        )
        string = string.replace("%d", str(self.denomination))
        string = string.replace(
            "%v", "Unknown value" if self.value is None else str(round(self.value,2))
        )
        string = string.replace(
            "%V", "Unknown value" if (self.value is None) else str(round(self.value*self.retention,2))
        )
        string = string.replace(
            "%y", "Unknown years" if self.years is None else self.yearsList()
        )
        string = string.replace(
            "%m", "Unknown metal" if self.metal is None else self.metalString()
        )
        string = string.replace("%f", str(self.fineness))
        string = string.replace("%F", str(self.fineness * 100))
        string = string.replace(
            "%a",
            "Unknown weight"
            if not isinstance(self.precious_metal_weight, weights.Weight)
            else f"{self.precious_metal_weight.as_troy_ounces()} toz",
        )
        string = string.replace(
            "%w",
            "Unknown weight"
            if not isinstance(self.weight, weights.Weight)
            else f"{self.weight.as_grams()}g",
        )
        string = string.replace("%n", "" if self.nickname is None else self.nickname)
        return string

    def __str__(self):
        if self.nickname is not None and self.nickname != "":
            return self.asAString("%n (%c) %d [%y] ... %a %m (%w @ %f%) - $%v")
        else:
            return self.asAString("(%c) %d [%y] ... %a %m (%w @ %f%) - $%v")
        """
        string = ""
        string += f"{'Unknown country' if self.country is None else f'({self.country.title()})'}"
        string += f" {self.denomination}"
        string += " Unknown years" if self.years is None else f' [{self.yearsList()}]'
        string += " ..."
        string += f" {self.metal.title()}"
        string += f" [fineness: {self.fineness}]"
        string += f" (weight: {'Unknown weight' if not isinstance(self.precious_metal_weight,weights.Weight) else f'{self.precious_metal_weight.as_troy_ounces()} toz'})"
        return string
        """
        # return f"[{'Unknown years' if self.years is None else self.yearsList()}] {self.denomination} ({'Unknown' if self.country is None else self.country.title()}) ... {self.metal.title()}[fineness:{self.fineness}](weight:{'Unknown weight' if not isinstance(self.precious_metal_weight,weights.Weight) else f'{self.precious_metal_weight.as_troy_ounces()} toz'})"
