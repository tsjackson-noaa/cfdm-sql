from __future__ import print_function
import datetime
import os
import unittest

import numpy

import cfdm

class CoordinateReferenceTest(unittest.TestCase):
    def setUp(self):
        self.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'test_file.nc')
        f = cfdm.read(self.filename)
        self.assertTrue(len(f)==1, 'f={}'.format(f))
        self.f = f[0]

        self.test_only = []
    #--- End: def

    def test_CoordinateReference__repr__str__dump(self):
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return

        f = self.f

        for cr in f.coordinate_references.values():
            _ = repr(cr)
            _ = str(cr)
            _ = cr.dump(display=False)
    #--- End: def

    def test_CoordinateReference_equals(self):
        f = self.f.copy()

        # Create a vertical grid mapping coordinate reference
        t = cfdm.CoordinateReference(
            coordinates=('coord1',),
            coordinate_conversion=cfdm.CoordinateConversion(
                parameters={'standard_name': 'atmosphere_hybrid_height_coordinate'},
                domain_ancillaries={'a': 'aux0', 'b': 'aux1', 'orog': 'orog'})
        )
        self.assertTrue(t.equals(t.copy(), verbose=True))
        
        # Create a horizontal grid mapping coordinate reference
        t = cfdm.CoordinateReference(
            coordinates=['coord1', 'fred', 'coord3'],
             coordinate_conversion=cfdm.CoordinateConversion(
                 parameters={'grid_mapping_name': 'rotated_latitude_longitude',
                             'grid_north_pole_latitude': 38.0,
                             'grid_north_pole_longitude': 190.0})
        )            
        self.assertTrue(t.equals(t.copy(), verbose=True))

        datum=cfdm.Datum(parameters={'earth_radius': 6371007})
        conversion=cfdm.CoordinateConversion(
            parameters={'grid_mapping_name': 'rotated_latitude_longitude',
                        'grid_north_pole_latitude': 38.0,
                        'grid_north_pole_longitude': 190.0})
        
        t = cfdm.CoordinateReference(
            coordinate_conversion=conversion,
            datum=datum,
            coordinates=['x', 'y', 'lat', 'lon']
        )

        self.assertTrue(t.equals(t.copy(), verbose=True))

        # Create a horizontal grid mapping coordinate reference
        t = cfdm.CoordinateReference(
               coordinates=['coord1', 'fred', 'coord3'],
               coordinate_conversion=cfdm.CoordinateConversion(
                   parameters={'grid_mapping_name': 'albers_conical_equal_area',
                               'standard_parallel': [-30, 10],
                               'longitude_of_projection_origin': 34.8,
                               'false_easting': -20000,
                               'false_northing': -30000})
        )
        self.assertTrue(t.equals(t.copy(), verbose=True))

        # Create a horizontal grid mapping coordinate reference
        t = cfdm.CoordinateReference(
               coordinates=['coord1', 'fred', 'coord3'],
               coordinate_conversion=cfdm.CoordinateConversion(
                   parameters={'grid_mapping_name': 'albers_conical_equal_area',
                               'standard_parallel': cfdm.Data([-30, 10]),
                               'longitude_of_projection_origin': 34.8,
                               'false_easting': -20000,
                               'false_northing': -30000})
        )
        self.assertTrue(t.equals(t.copy(), verbose=True))
    #--- End: def

    def test_CoordinateConversion(self):
        if self.test_only and inspect.stack()[0][3] not in self.test_only:
            return

        f = self.f

        cr = f.construct('standard_name:atmosphere_hybrid_height_coordinate')
        cc = cr.coordinate_conversion
        _ = repr(cc)
        _ = str(cc)
    #--- End: def

#--- End: class

if __name__ == '__main__':
    print('Run date:', datetime.datetime.now())
    print(cfdm.environment())
    print('')
    unittest.main(verbosity=2)
