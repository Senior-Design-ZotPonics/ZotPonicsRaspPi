class ZotPonics():
    def __init__(self):
        pass

    def run(self,temperSim=False,humidSim=False,baseLevelSim=False,ecSim=False):
        """
        temperSim<bool>:
        humidSim<bool>:
        baseLevelSim<bool>:
        ecSim<bool>:
        """
        #===========Data Collection=============
        #------Temperature Data (C)--------
        temperature = self.temperData(temperSim)

        #------Humidity Data (%)--------
        humdity = self.humidData(humidSim)

        #------Base Reservoir Water Level Data (cm)--------
        baseLevel = self.baseLevelData(baseLevelSim)

        #------EC Sensor(ppm)----------------
        ec = self.ecData(ecSim)

        #-----------Add to Database----------

        #===========Engage Actuators Logic=============

    def temperData(self,simulate):
        """
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

    def humidData(self,simulate):
        """
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

    def baseLevelData(self,simulate):
        """
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

    def ecData(self,simulate):
                """
                simulate<bool>:
                """
                if simulate:
                    return 0.0
                else:
                    #this would be where we implement sensor GPIO logic
                    return 0.0 #temporary

    def updateDatabase(self):
        """
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

if __name__ == "__main__":
    zot = ZotPonics()
    zot.run()
