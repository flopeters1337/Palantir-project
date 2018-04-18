
import warnings


class Device:
    def __init__(self, json_obj: dict):
        """JSON constructor

        :param json_obj:    A valid contractDTD JSON object.
        """
        self.alias = None
        self.type = None
        self.location = None
        self.sensors = dict()
        self.actuators = dict()

        self.initialize(type=json_obj['type'],
                        sensors=json_obj['sensors']
                        if 'sensors' in json_obj.keys() else None,
                        actuators=json_obj['actuators']
                        if 'actuators' in json_obj.keys() else None,
                        alias=json_obj['alias']
                        if 'alias' in json_obj.keys() else None,
                        location=json_obj['location']
                        if 'location' in json_obj.keys() else None)

    def initialize(self, type: str, sensors: list = None,
                   actuators: list = None, alias: str = None,
                   location: str = None):
        """Initialize the Device object.

        :param type:        The type of the device (either 'static' or
                            'dynamic'). Raises an exception otherwise.
        :param location:    Location of the device if it is static. Is ignored
                            if the device is dynamic.
        :param sensors:     List of sensorDTD JSON objects representing the
                            device's available sensors.
        :param actuators:   List of actuatorDTD JSON objects representing the
                            device's available actuators and their
                            corresponding parameters.
        :param alias:       Potential LAN alias for the device to communicate
                            with it instead of its IP address.
        """
        self.alias = alias

        if type != 'static' and type != 'dynamic':
            raise ValueError('Incorrect type for sensor')
        self.type = type

        if type == 'dynamic' and location is not None:
            warnings.warn('Type of device is static, location silently '
                          'ignored')
            self.location = None
        else:
            self.location = location

        # Build sensors dictionary
        if sensors is not None:
            for sensor in sensors:
                self.sensors[sensor['name']] = sensor['return_type']

        # Build actuators dictionary
        if actuators is not None:
            for actuator in actuators:
                self.actuators[actuator['name']] = dict()
                for param in actuator['parameters']:
                    self.actuators[actuator['name']][param['name']] = {
                        'optional': param['optional'],
                        'type': param['type'],
                        'domain': param['domain']
                    }

    def get_sensors(self):
        """Get the list of the device's sensors.

        :return:    A list of names of the device's sensors.
        """
        return list(self.sensors.keys())

    def get_actuators(self):
        """Get the list of the device's actuators.

        :return:    A list of names of the device's actuators.
        """
        return list(self.actuators.keys())

    def check_actuator_params(self, actuator_name: str, parameters: list):
        """Check if the parameters given as arguments are suitable for a given
        actuator.

        :param actuator_name:   One of the device's actuators name.
        :param parameters:      A list of pairs consisting of parameter name
                                and a value for that parameter. (e.g.
                                [('coffee', 'brew')] )
        :return:    True if the list of parameters with values is valid for the
                    given actuator.
        """
        actuator = self.actuators[actuator_name]

        # Check if all required parameters are present
        required_params = set([x['name'] for x in actuator['parameters']
                               if not x['optional']])
        param_set = set(x for x, _ in parameters)
        if required_params.issubset(param_set):
            return False

        for param_name, param_value in parameters:
            # Type check
            param_type = actuator[param_name]['type']
            if type(param_value) != "<class '" + param_type + "'>":
                return False

            # Domain check
            if 'domain' in actuator[param_name].keys():
                param_domain = actuator[param_name]['domain']
                if type(param_domain) == list:
                    if param_value not in param_domain:
                        return False
                elif type(param_domain) == dict:
                    if param_value > param_domain['max'] or \
                       param_value < param_domain['min']:
                        return False
                else:
                    raise TypeError('Parameter domain should be a list or '
                                    'dictionary. Found : '
                                    + str(type(param_domain)))

        return True
