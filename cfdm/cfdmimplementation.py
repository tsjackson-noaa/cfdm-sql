from . import (AuxiliaryCoordinate,
               CellMethod,
               CellMeasure,
               CoordinateReference,
               DimensionCoordinate,
               DomainAncillary,
               DomainAxis,
               Field,
               FieldAncillary,
               Bounds,
               InteriorRing,
               CoordinateConversion,
               Datum,
               Count,
               List,
               Index,
               NodeCountProperties,
               PartNodeCountProperties)

from .data import (Data,
                   GatheredArray,
                   NetCDFArray,
                   RaggedContiguousArray,
                   RaggedIndexedArray,
                   RaggedIndexedContiguousArray)

from .abstract import Implementation

from . import CF


class CFDMImplementation(Implementation):
    ''''A container for the CF data model implementation.

    .. versionadded:: 1.7.0

    '''
    def __init__(
            self,

            cf_version=None,

            AuxiliaryCoordinate=None,
            CellMeasure=None,
            CellMethod=None,
            CoordinateReference=None,
            DimensionCoordinate=None,
            DomainAncillary=None,
            DomainAxis=None,
            Field=None,
            FieldAncillary=None,

            Bounds=None,
            InteriorRing=None,
            CoordinateConversion=None,
            Datum=None,
            Data=None,

            GatheredArray=None,
            NetCDFArray=None,
            RaggedContiguousArray=None,
            RaggedIndexedArray=None,
            RaggedIndexedContiguousArray=None,

            List=None,
            Count=None,
            Index=None,
            NodeCountProperties=None,
            PartNodeCountProperties=None,
    ):
        '''**Initialisation**

    :Parameters:

        AuxiliaryCoordinate:
            An auxiliary coordinate construct class.

        CellMeasure:
            A cell measure construct class.

        CellMethod:
            A cell method construct class.

        CoordinateReference:
            A coordinate reference construct class.

        DimensionCoordinate:
            A dimension coordinate construct class.

        DomainAncillary:
            A domain ancillary construct class.

        DomainAxis:
            A domain axis construct class.

        Field:
            A field construct class.

        FieldAncillary:
            A field ancillary construct class.

        Bounds:             = Bounds
        CoordinateAncillary = CoordinateAncillary
        Data                = Data
        NetCDF              = NetCDF

        '''
        super().__init__(
            cf_version=cf_version,

            AuxiliaryCoordinate=AuxiliaryCoordinate,
            CellMeasure=CellMeasure,
            CellMethod=CellMethod,
            CoordinateReference=CoordinateReference,
            DimensionCoordinate=DimensionCoordinate,
            DomainAncillary=DomainAncillary,
            DomainAxis=DomainAxis,
            Field=Field,
            FieldAncillary=FieldAncillary,

            Bounds=Bounds,
            InteriorRing=InteriorRing,
            CoordinateConversion=CoordinateConversion,
            Datum=Datum,
            Data=Data,

            GatheredArray=GatheredArray,
            NetCDFArray=NetCDFArray,
            RaggedContiguousArray=RaggedContiguousArray,
            RaggedIndexedArray=RaggedIndexedArray,
            RaggedIndexedContiguousArray=RaggedIndexedContiguousArray,

            List=List,
            Count=Count,
            Index=Index,
            NodeCountProperties=NodeCountProperties,
            PartNodeCountProperties=PartNodeCountProperties,
        )

    def __repr__(self):
        '''Called by the `repr` built-in function.

    x.__repr__() <==> repr(x)

        '''
        return '<{0}: >'.format(self.__class__.__name__)

    def bounds_insert_dimension(self, bounds, position):
        '''Insert a new dimension into bounds data.

    :Parameters:

        bounds: bounds component

        position: `int`

    :Returns:

        Bounds component

        '''
        return bounds.insert_dimension(position=position)

    def conform_geometry_variables(self, field):
        '''Collate geometry variable properties.

    .. versionadded:: 1.8.0

    :Parameters:

        field: field construct

    :Returns:

        `bool`

        '''
        out = {'node_count': {},
               'part_node_count': {},
               'interior_ring': {}}

        for coord in self.get_auxiliary_coordinates(field).values():
            for variable in out:
                x = getattr(self, 'get_'+variable)(coord)
                if x is None:
                    continue

                for k, v in x.properties().items():
                    if k not in out[variable]:
                        out[variable][k] = v
                    elif v != out[variable][k]:
                        return False
        # --- End: for

        for coord in self.get_auxiliary_coordinates(field).values():
            for variable in out:
                x = getattr(self, 'get_'+variable)(coord)
                if x is None:
                    continue

                x.set_properties(out[variable])
        # --- End: for

        return True

    def construct_insert_dimension(self, construct, position):
        '''Insert a new dimension into metedata construct data.

    :Parameters:

        construct: construct

        position: `int`

    :Returns:

        construct

        '''
        return construct.insert_dimension(position=position)

    def copy_construct(self, construct):
        '''Return a deep copy of a construct.

    :Returns:

            The deep copy.

        '''
        return construct.copy()

    def convert(self, field=None, construct_id=None):
        '''Convert a metadata construct into a field construct.

    :Parameters:

        field: field construct

        construct_id: `str`

    :Returns:

        Field construct

        '''
        return field.convert(construct_id, full_domain=False)

    def data_insert_dimension(self, data, position):
        '''Insert a new dimension into a data array.

    :Parameters:

        bounds: data

        position: `int`

    :Returns:

            The new data array

        '''
        return data.insert_dimension(position=position)

    def del_property(self, construct, prop, default):
        ''''Remove a property from a construct.

    :Parameters:

        construct: construct

        prop: `str`

        default: optional

    :Returns:

            The value of the deleted property

        '''
        return construct.del_property(prop, default)

    def field_insert_dimension(self, field, position=0, axis=None):
        '''Insert a new dimension into field construct data.

    :Parameters:

        field: field construct

        position: `int`

        axis: optional

    :Returns:

        field construct
        '''
        return field.insert_dimension(axis, position=position)

    def get_array(self, data):
        '''Return the data as a `numpy` array.

    :Parameters:

        data: data instance

    :Returns:

        `numpy.ndarray`

        '''
        return data.array

    def get_auxiliary_coordinates(self, field, axes=[], exact=False):
        '''Return auxiliary coordinate constructs that span particular axes.

    If no axes are specified then all auxiliary coordinate constructs
    are returned.

    If axes are specified then auxiliary coordinate constructs whose
    data arrays span those axes, and possibly other axes, are
    returned.

    :Parameters:

        axes: sequence of `str`

    :Returns:

        `dict`

        '''
        if exact:
            arg = 'exact'
        else:
            arg = 'and'

        return dict(field.auxiliary_coordinates.filter_by_axis(
            arg, *axes))

    def get_bounds(self, parent, default=None):
        '''Return the bounds of a construct.

    :Parameters:

        parent: construct with bounds

        default: optional

    :Returns:

        Bounds component

        '''
        return parent.get_bounds(default=default)

    def get_bounds_ncvar(self, parent, default=None):
        '''Return the netCDF variable name of the bounds.

    :Parameters:

        parent: construct with bounds

        default: optional

    :Returns:

        `str`

        '''
        bounds = parent.get_bounds(None)
        if bounds is None:
            return default

        return self.nc_get_variable(bounds, default=default)

    def get_cell_measures(self, field):
        '''Return all of the cell measure constructs of a field.

    :Parameters:

        field: field construct

    :Returns:

        '''
        return field.cell_measures

    def get_cell_methods(self, field):
        '''Return all of the cell method constructs of a field.

    :Parameters:

        field: field construct

    :Returns:

        '''
        return field.cell_methods.ordered()

    def get_cell_method_axes(self, cell_method, default=None):
        '''Return the axes of a cell method construct.

    :Parameters:

        cell_method: cell method construct

        default: optional

    :Returns:

        `tuple`

        '''
        return cell_method.get_axes(default=default)

    def get_cell_method_string(self, cell_method):
        '''Return the `str` representation of a cell method construct.

    :Parameters:

        cell_method: cell method construct

    :Returns:

        `str`

        '''
        return str(cell_method)

    def get_cell_method_qualifiers(self, cell_method):
        '''Return the `str` representation of a cell method construct.

    :Parameters:

        cell_method: cell method construct

    :Returns:

        `str`

        '''
        return cell_method.qualifiers()

    def get_compressed_array(self, data):
        '''Return the data in its compressed form .

    :Parameters:

        data: data instance

    :Returns:

        `numpy.ndarray`

        '''
        return data.compressed_array

    def get_compressed_axes(self, field, key=None, construct=None):
        '''Return the indices of the compressed axes.

    :Parameters:

        field: field construct

        key: `str`, optional

        construct: optional

    :Returns:

        `list` of `int`

        '''
        if construct is not None:
            data = self.get_data(construct)
        else:
            data = self.get_data(field)

        if key is not None:
            data_axes = self.get_construct_data_axes(field, key)
        else:
            data_axes = self.get_field_data_axes(field)

        return [data_axes[i] for i in self.get_data_compressed_axes(data)]

    def get_compression_type(self, construct):
        '''Return the construct keys of the domain axis constructs spanned by
    a metadata construct.

    :Parameters:

        field: field construct

        key: `str`

    :Returns:

        `tuple`

        '''
        data = construct.get_data(None)
        if data is None:
            return ''

        return data.get_compression_type()

    def get_construct_data_axes(self, field, key):
        '''Return the construct keys of the domain axis constructs spanned by
    a metadata construct.

    :Parameters:

        field: field construct

        key: `str`

    :Returns:

        `tuple`

        '''
        return field.constructs.data_axes()[key]

    def get_constructs(self, field, axes=[], data=False):
        '''Return constructs that span particular axes.

    If no axes are specified then all constructs are returned.

    If axes are specified then constructs whose data arrays span those
    axes, and possibly other axes, are returned.

    :Parameters:

        axes: sequence of `str`

        data: `bool`
            If True then only return constructs that can contain data.

    :Returns:

        `dict`

        '''
        if data:
            return dict(field.constructs.filter_by_data())

        return dict(field.constructs.filter_by_axis('and', *axes))

    def get_coordinate_reference_coordinates(self, coordinate_reference):
        '''Return the coordinates of a coordinate reference construct.

    :Parameters:

        coordinate_reference: coordinate reference construct

    :Returns:

        `set`

        '''
        return coordinate_reference.coordinates()

    def get_coordinate_conversion_parameters(self, coordinate_reference):
        '''Return the coordinate conversion parameters of a coordinate
    reference construct.

    :Parameters:

        coordinate_reference: coordinate reference construct

    :Returns:

        `dict`

        '''
        return coordinate_reference.coordinate_conversion.parameters()

    def get_coordinate_references(self, field):
        '''Return all of the coordinate reference constructs of a field.

    :Parameters:

        field: field construct

    :Returns:

        '''
        return field.coordinate_references

    def get_coordinates(self, field):
        '''Return all of the coordinate constructs of a field.

    :Parameters:

        field: field construct

    :Returns:

        '''
        return field.coordinates

    def get_data_calendar(self, data, default=None):
        '''Return the calendar of date-time data.

    :Parameters:

        data: `data instance

        default: optional

    :Returns:

        `str`

        '''
        return data.get_calendar(default=default)

    def get_data_compressed_axes(self, data):
        '''Return the indices of the compressed axes.

    :Parameters:

        data: data instance

    :Returns:

        `list` of `int`

        '''
        return data.get_compressed_axes()

    def get_data_ndim(self, parent):
        '''Return the number of dimensions spanned by the data array.

    :Parameters:

        parent:
            The object containing the data array.

    :Returns:

        `int`
            The number of dimensions spanned by the data array.

    **Examples:**

    >>> d
    <DimensionCoordinate: latitude(180) degrees_north>
    >>> w.get_data_ndim(d)
    1

    >>> b
    <Bounds: latitude(180, 2) degrees_north>
    >>> w.get_data_ndim(b)
    2

        '''
        return parent.data.ndim

    def get_data_shape(self, parent, isdata=False):
        '''Return the shape of the data array.

    :Parameters:

        parent:
            The object containing the data array.

        isdata: `bool`
            If True then the prent is already a data object

    :Returns:

        `tuple`
            The shape of the data array.

    **Examples:**

    >>> d
    <DimensionCoordinate: latitude(180) degrees_north>
    >>> w.get_data_shape(d)
    (180,)

    >>> b
    <Bounds: latitude(180, 2) degrees_north>
    >>> w.get_data_shape(b)
    (180, 2)

        '''
        if isdata:
            return parent.shape

        return parent.data.shape

    def get_data_size(self, parent):
        '''Return the number of elements in the data array.

    :Parameters:

        parent:
            The object containing the data array.

    :Returns:

        `int`
            The number of elements in the data array.

    **Examples:**

    >>> d
    <DimensionCoordinate: latitude(180) degrees_north>
    >>> w.get_data_ndim(d)
    180

    >>> b
    <Bounds: latitude(180, 2) degrees_north>
    >>> w.get_data_ndim(b)
    360
        '''
        return parent.data.size

    def get_data_units(self, data, default=None):
        '''Return the units of data.

    :Parameters:

        data: data instance

        default: optional

    :Returns:

        `str`

        '''
        return data.get_units(default=default)

    def get_datum(self, coordinate_reference):
        '''Return the datum of a coordiante reference construct.

    :Parameters:

          coordinate_reference: coordinate reference construct

    :Returns:

        Datum component

        '''
        return coordinate_reference.datum

    def get_datum_parameters(self, ref):
        '''Return the parameter-valued terms of a coordinate reference datum.

    :Parameters:

        coordinate_reference: `CoordinateReference`

    :Returns:

        `dict`

        '''
        return ref.datum.parameters()

    def get_dimension_coordinates(self, field):
        '''Return all of the dimension coordinate constructs of a field.

    :Parameters:

        field: field construct

    :Returns:

        '''
        return field.dimension_coordinates

    def get_domain_ancillaries(self, field):
        '''Return all of the domain ancillary constructs of a field.

    :Parameters:

        field: field construct

    :Returns:

        '''
        return field.domain_ancillaries

    def get_domain_axes(self, field):
        '''Return all of the domain axis constructs of a field.

    :Parameters:

        field: field construct

    :Returns:

        '''
        return field.domain_axes

    def get_domain_axis_size(self, field, axis):
        '''Return the size a of domrain axis construct.

    :Parameters:

        field: field construct

        axis: `str`

    :Returns:

        '''
        return field.domain_axes[axis].get_size()

    def get_sample_dimension_position(self, construct):
        '''Return the position of the sample dimension of compressed data.

    :Parameters:

        construct: construct

    :Returns:

        `int`

        '''
        return construct.get_data().get_compressed_dimension()

    def nc_get_geometry_variable(self, field, default=None):
        '''Return the netCDF variable name of the geometry container.

    .. versionadded:: 1.8.0

    :Parameters:

    :Returns:

        `str`

        '''
        return field.nc_get_geometry_variable(default)

    def nc_get_group_attributes(self, field):
        '''Return the netCDF sub-group attribtues for the field construct.

    .. versionadded:: 1.8.6

    :Parameters:

        field: field construct

    :Returns:

        `dict`

        '''
        return field.nc_group_attributes()

    def nc_get_variable_groups(self, field):
        '''Return the netCDF groups for the field construct.

    .. versionadded:: 1.8.6

    :Parameters:

        field: field construct

    :Returns:

        `tuple`

        '''
        return field.nc_variable_groups()

    def nc_get_hdf5_chunksizes(self, data):
        '''Return the HDF5 chunksizes for the data.

    ..versionadded:: 1.7.2

    :Parameters:

        data: Data instance

    :Returns:

        `tuple` or `None`
            The HDF5 chunksizes, or `None` if they haven't been set.

        '''
        out = data.nc_hdf5_chunksizes()
        if not out:
            out = None

        return out

    def nc_get_sample_dimension(self, count, default=None):
        '''Return the name of the netCDF sample dimension.

    :Returns:

        `str`
            The name of the netCDF sample dimension.

        '''
        return count.nc_get_sample_dimension(default=default)

    def nc_is_unlimited_axis(self, field, axis):
        '''Whether a domain axis corresponds to a netCDF unlimited dimension.

    .. versionadded:: 1.7.0

    :Parameters:

        field: `Field`

    :Returns:

        `set`
            The selection of domain axis construct identifiers that are
            unlimited.

        '''
        domain_axis = field.constructs.get(axis)
        if domain_axis is None:
            return False

        return domain_axis.nc_is_unlimited()

    def nc_set_unlimited_axis(self, field, axis):
        '''Set a domain axis to correspond to a netCDF unlimited dimension.

    .. versionadded:: 1.7.4

    :Parameters:

        field: `Field`

        axis: `str`
            Domain axis construct key.

    :Returns:

        `None`

        '''
        domain_axis = field.constructs.get(axis)
        if domain_axis is None:
            return

        domain_axis.nc_set_unlimited(True)

    def nc_get_global_attributes(self, field):
        '''Return the netCDF global attributes.

    :Parameters:

        field: field construct

    :Returns:

        `dict`

        '''
        return field.nc_global_attributes()

    def nc_set_global_attributes(self, field, attributes):
        '''Set netCDF global attributes.

    .. versionadded:: 1.7.0

    :Parameters:

        field: field construct

        attributes: `dict`

    :Returns:

        `None`

        '''
        for attr, value in attributes.items():
            field.nc_set_global_attribute(attr, value)

    def nc_set_group_attributes(self, field, attributes):
        '''Set netCDF group attributes.

    .. versionadded:: 1.8.6

    :Parameters:

        field: field construct

        attributes: `dict`

    :Returns:

        `None`

        '''
        for attr, value in attributes.items():
            field.nc_set_group_attribute(attr, value)

    def equal_components(self, construct0, construct1,
                         ignore_type=False):
        '''Whether or not two field construct components are equal.

    A "component" is either a metadata construct or a metadata
    construct component (such as a bounds component).

    .. versionadded::: 1.8.6

    :Parameter:

        construct0: construct

        construct1: construct

        ignore_type: `bool`, optional

    :Retuns:

        `bool`

        '''
        return construct0.equals(construct1, ignore_type=ignore_type,
                                 verbose=0)

    def equal_constructs(self, construct0, construct1,
                         ignore_type=False):
        '''Whether or not two field construct components are equal.

    A "component" is either a metadata construct or a metadata
    construct component (such as a bounds component).

    .. versionadded::: 1.7.0

    :Parameter:

        construct0: construct

        construct1: construct

        ignore_type: `bool`, optional

    :Retuns:

        `bool`

        '''
        raise NotImplementedError("Deprecated at version 1.8.6. "
                                  + "Use 'equal_components' instead.")

    def equal_properties(self, property_value0, property_value1):
        '''Whether or not two property values are equal.

    :Parameter:

        property_value0:

        property_value1:

    :Retuns:

        `bool`

        '''
        field = self.get_class('Field')()
        return field._equals(property_value0, property_value1)

    def equal_datums(self, coordinate_reference0, coordinate_reference1):
        '''Whether or not two coordinate reference datums are equal.

    :Parameters:

        coordinate_reference0: coordinate reference construct

        coordinate_reference1: coordinate reference construct

    :Returns:

        `bool`

        '''
        datum0 = coordinate_reference0.datum
        datum1 = coordinate_reference1.datum
        return datum0.equals(datum1)

    def get_construct_data_size(self, construct):
        '''Return the size of a construct's data.

    :Parameters:

        construct: construct

    :Returns:

        `int`

        '''
        return construct.data.size

    def nc_get_external(self, parent):
        '''Return whether a construct is external.

    :Parameters:

        parent:
            The object

    :Returns:

        `bool`
            Whether the construct is external.

        '''
        if not hasattr(parent, 'nc_get_external'):
            return False

        return parent.nc_get_external()

    def get_field_ancillaries(self, field):
        '''Return the field ancillaries of a field.

    :Parameters:

        field:
            The field object.

    :Returns:

        `dict`
            A dictionary whose values are field ancillary objects, keyed
            by unique identifiers.

    **Examples:**

    >>> w.get_field_ancillaries(f)
    {'fieldancillary0': <FieldAncillary: ....>,
     'fieldancillary1': <FieldAncillary: ....>}

        '''
        return field.field_ancillaries

    def get_field_data_axes(self, field):
        '''Return the construct keys of the field constructs data dimensions.

    :Parameters:

        field: field construct

    :Returns:

        `tuple`

        '''
        return field.get_data_axes()

    def get_filenames(self, parent):
        '''Return the name of the file or files containing the data.

    :Parameters:

        parent:

    :Returns:

        `set`

        '''
        return parent.get_filenames()

    def get_data_max(self, parent):
        '''Use `get_data_maximum` instead (since cfdm version 1.8.0).

        '''
        raise NotImplementedError(
            "Use `get_data_maximum` instead (since cfdm version 1.8.0).")

    def get_data_maximum(self, parent):
        '''Return the maximum value of the data.

    :Parameters:

        parent:

    :Returns:

        Data instance

        '''
        return parent.data.maximum()

    def get_data_sum(self, parent):
        '''Return the sum of the data.

    :Parameters:

        parent:

    :Returns:

        Data instance

        '''
        return parent.data.sum()

    def get_count(self, construct):
        '''Return the count variable of compressed data.

    :Parameters:

        construct: construct

    :Returns:

        Count variable or `None`

        '''
        return construct.get_data().get_count(default=None)

    def get_index(self, construct):
        '''Return the index variable of compressed data.

    :Parameters:

        construct: construct

    :Returns:

        Index variable or `None`

        '''
        return construct.get_data().get_index(default=None)

    def get_inherited_properties(self, parent):
        '''Return all inherited properties.

    .. versionadded:: 1.8.6

    :Parameters:

        parent:
            The object that inherits the properties.

    :Returns:

        `dict`
            The inherited property names and their values

        '''
        return parent.inherited_properties()

    def get_interior_ring(self, construct):
        '''Return the interior ring variable of geometry coordinates.

    :Parameters:

        construct: construct

    :Returns:

        Interior ring variable or `None`

        '''
        return construct.get_interior_ring(default=None)

    def get_list(self, construct):
        '''Return the list variable of compressed data.

    :Parameters:

        construct: construct

    :Returns:

        List variable or `None`

        '''
        return construct.get_data().get_list(default=None)

    def get_measure(self, cell_measure):
        '''Return the measure property of a cell measure construct.

    :Parameters:

        cell_measure:
            The cell measure object.

    :Returns:

        `str` or `None`
            The measure property, or `None` if it has not been set.

    **Examples:**

    >>> c
    <CellMeasure: area(73, 96) km2>
    >>> w.get_measure(c)
    'area'
        '''
        return cell_measure.get_measure(default=None)

    def nc_get_dimension(self, parent, default=None):
        '''Return the netCDF variable name.

    :Parameters:

        parent:
            The object containing the data array.

        default: `str`, optional

    :Returns:

        `str`
            The netCDF dimension name.

        '''
        return parent.nc_get_dimension(default=default)

    def nc_get_variable(self, construct, default=None):
        '''Return the netCDF variable name.

    :Parameters:

        parent:

        default: `str`, optional

    :Returns:

        `str`
            The netCDF variable name.

        '''
        return construct.nc_get_variable(default=default)

    def get_node_count(self, construct):
        '''Return the node count variable of geometry coordinates.

    .. versionadded:: 1.8.0

    :Parameters:

        construct: construct

    :Returns:

        Node count variable or `None`

        '''
        return construct.get_node_count(default=None)

    def get_part_node_count(self, construct):
        '''Return the part node count variable of geometry coordinates.

    .. versionadded:: 1.8.0

    :Parameters:

        construct: construct

    :Returns:

        Part node count variable or `None`

        '''
        return construct.get_part_node_count(default=None)

    def get_properties(self, parent):
        '''Return all properties.

    :Parameters:

        parent:
            The object containing the properties.

    :Returns:

        `dict`
            The property names and their values

    **Examples:**

    >>> d
    <DimensionCoordinate: latitude(180) degrees_north>
    >>> w.get_properties(d)
    {'units: 'degrees_north'}
     'standard_name: 'latitude',
     'foo': 'bar'}
        '''
        return parent.properties()

    def get_property(self, construct, prop, default=None):
        '''Return a property of a construct.

    :Parameters:

        construct:

        prop: `str`

        default: optional

    :Returns:

            The property value.

        '''
        return construct.get_property(prop, default=default)

    def get_geometry(self, construct, default=None):
        '''Return the geometry type of coordinates.

    :Parameters:

        construct:

        default: optional

    :Returns:

        `str` or `None`
            The geometry type.

        '''
        return construct.get_geometry(default=default)

    def get_data(self, parent, default=None):
        '''Return the data array.

    :Parameters:

        parent:
            The object containing the data array.

    :Returns:

            The data.

    **Examples:**

    >>> d
    <DimensionCoordinate: latitude(180) degrees_north>
    >>> w.get_data(d)
    <Data(180): [-89.5, ..., 89.5] degrees_north>

    >>> b
    <Bounds: latitude(180, 2) degrees_north>
    >>> w.get_data(b)
    <Data(180, 2): [[-90, ..., 90]] degrees_north>
        '''
        return parent.get_data(default=default)

    def initialise_AuxiliaryCoordinate(self):
        '''Return an auxiliary coordinate construct.

    :Returns:

        Auxiliary coordinate construct

        '''
        cls = self.get_class('AuxiliaryCoordinate')
        return cls()

    def initialise_Bounds(self):
        '''Return a bounds component.

    :Returns:

        Bounds component

        '''
        cls = self.get_class('Bounds')
        return cls()

    def initialise_CellMeasure(self, measure=None):
        '''Return a cell measure construct.

    :Parameters:

        measure: `str`, optional

    :Returns:

        Cell measure construct

        '''
        cls = self.get_class('CellMeasure')
        return cls(measure=measure)

    def initialise_CellMethod(self, axes=None, method=None,
                              qualifiers=None):
        '''Return a cell method construct.

    :Parameters:

        axes: optional

        method: `str`, optional

        qualifiers: `dict`, optional

    :Returns:

        Cell method construct

        '''
        cls = self.get_class('CellMethod')
        return cls(axes=axes, method=method, qualifiers=qualifiers)

    def initialise_CoordinateConversion(self,
                                        domain_ancillaries=None,
                                        parameters=None):
        '''Return a coordinate conversion component.

    :Parameters:

        domain_ancillaries: optional

        parameters: optioanl

    :Returns:

        Coordinate conversion component

        '''
        cls = self.get_class('CoordinateConversion')
        return cls(domain_ancillaries=domain_ancillaries,
                   parameters=parameters)

    def initialise_CoordinateReference(self):
        '''Return a coordinate reference construct.

    :Returns:

        Coordinate reference construct

        '''
        cls = self.get_class('CoordinateReference')
        return cls()

    def initialise_Count(self):
        '''Return a count variable.

    :Returns:

        Count variable

        '''
        cls = self.get_class('Count')
        return cls()

    def initialise_Data(self, array=None, units=None, calendar=None,
                        copy=True, **kwargs):
        '''Return a data instance.

    :Parameters:

        array: optional

        units: optional

        calendar: optional

        copy: `bool`, optional

        kwargs: optional

    :Returns:

        Data instance

        '''
        cls = self.get_class('Data')
        return cls(array=array, units=units, calendar=calendar,
                   copy=copy, **kwargs)

    def initialise_Datum(self, parameters=None):
        '''Return a coordinate conversion component.

    :Parameters:

        parameters: optioanl

    :Returns:

        Datum component

        '''
        cls = self.get_class('Datum')
        return cls(parameters=parameters)

    def initialise_DimensionCoordinate(self, properties=None,
                                       data=None, bounds=None,
                                       interior_ring=None, copy=True):
        '''Return a dimension coordinate construct.

    :Parameters:

        properties: `dict`, optional

        data: optional

        bounds: optional

        interior_ring: optional

        copy: `bool`, optional

    :Returns:

        Dimension coordinate construct

        '''
        cls = self.get_class('DimensionCoordinate')
        return cls(properties=properties, data=data, bounds=bounds,
                   interior_ring=interior_ring, copy=copy)

    def initialise_DimensionCoordinate_from_AuxiliaryCoordinate(
            self,
            auxiliary_coordinate=None,
            copy=True):
        '''Return a dimension coordinate construct insitialized from an
    auxiliary coordinate construct.

    :Parameters:

        auxiliary_coordinate: auxiliary coordiante consturct

        copy: `bool`,optional

    :Returns:

        Dimension coordinate construct

        '''
        cls = self.get_class('DimensionCoordinate')
        return cls(source=auxiliary_coordinate, copy=copy)

    def initialise_DomainAncillary(self):
        '''Return a domain ancillary construct.

    :Returns:

        Domain ancillary construct

        '''
        cls = self.get_class('DomainAncillary')
        return cls()

    def initialise_DomainAxis(self, size=None):
        '''Return a domain ancillary construct.

    :Returns:

        Domain ancillary construct

        '''
        cls = self.get_class('DomainAxis')
        return cls(size=size)

    def initialise_Field(self):
        '''Return a field qconstruct.

    :Returns:

        Field construct

        '''
        cls = self.get_class('Field')
        return cls()

    def initialise_FieldAncillary(self):
        '''Return a field ancillary construct.

    :Returns:

        Field ancillary construct

        '''
        cls = self.get_class('FieldAncillary')
        return cls()

    def initialise_GatheredArray(self, compressed_array=None,
                                 ndim=None, shape=None, size=None,
                                 compressed_dimension=None,
                                 list_variable=None):
        '''Return a gathered array instance.

    :Parameters:

        compressed_array: optional

        ndim: `int`, optional

        shape: sequence of `int`, optional

        size: `int, optional

        compressed_dimension: `int`, optional

        list_variable: optional

    :Returns:

        Gathered array

        '''
        cls = self.get_class('GatheredArray')
        return cls(compressed_array=compressed_array, ndim=ndim,
                   shape=shape, size=size,
                   compressed_dimension=compressed_dimension,
                   list_variable=list_variable)

    def initialise_Index(self):
        '''Return an index variable.

    :Returns:

        Index variable

        '''
        cls = self.get_class('Index')
        return cls()

    def initialise_InteriorRing(self):
        '''Return an interior ring variable.

    :Returns:

        Interior ring variable

        '''
        cls = self.get_class('InteriorRing')
        return cls()

    def initialise_List(self):
        '''Return a list variable.

    :Returns:

        List variable

        '''
        cls = self.get_class('List')
        return cls()

    def initialise_NetCDFArray(self, filename=None, ncvar=None,
                               group=None, dtype=None, ndim=None,
                               shape=None, size=None, mask=True):
        '''Return a netCDF array instance.

    :Parameters:

        filename: `str`

        ncvar: `str`

        group: `None` or sequence of str`

        dytpe: `numpy.dtype`

        ndim: `int`, optional

        shape: sequence of `int`, optional

        size: `int, optional

        mask: `bool`, optional

    :Returns:

        NetCDF array instance

        '''
        cls = self.get_class('NetCDFArray')
        return cls(filename=filename, ncvar=ncvar, group=group,
                   dtype=dtype, ndim=ndim, shape=shape, size=size,
                   mask=mask)

    def initialise_NodeCount(self):
        '''Return a node count properties variable.

    :Returns:

        Node count properties bariable

        '''
        cls = self.get_class('NodeCountProperties')
        return cls()

    def initialise_PartNodeCount(self):
        '''Return a part node count properties variable.

    :Returns:

        Part node count properties variable

        '''
        cls = self.get_class('PartNodeCountProperties')
        return cls()

    def initialise_RaggedContiguousArray(self, compressed_array=None,
                                         ndim=None, shape=None,
                                         size=None,
                                         count_variable=None):
        '''Return a ragged contigous array instance.

    :Parameters:

        compressed_array: optional

        ndim: `int`, optional

        shape: sequence of `int`, optional

        size: `int, optional

        compressed_dimension: `int`, optional

        count_variable: optional

    :Returns:

        Ragged contigous array

        '''
        cls = self.get_class('RaggedContiguousArray')
        return cls(compressed_array=compressed_array, ndim=ndim,
                   shape=shape, size=size,
                   count_variable=count_variable)

    def initialise_RaggedIndexedArray(self, compressed_array=None,
                                      ndim=None, shape=None,
                                      size=None, index_variable=None):
        '''Return a ragged indexed array instance.

    :Parameters:

        compressed_array: optional

        ndim: `int`, optional

        shape: sequence of `int`, optional

        size: `int, optional

        compressed_dimension: `int`, optional

        index_variable: optional

    :Returns:

        Ragged indexed array

        '''
        cls = self.get_class('RaggedIndexedArray')
        return cls(compressed_array=compressed_array, ndim=ndim,
                   shape=shape, size=size,
                   index_variable=index_variable)

    def initialise_RaggedIndexedContiguousArray(self,
                                                compressed_array=None,
                                                ndim=None, shape=None,
                                                size=None,
                                                count_variable=None,
                                                index_variable=None):
        '''Return a ragged indexed contiguous array instance.

    :Parameters:

        compressed_array: optional

        ndim: `int`, optional

        shape: sequence of `int`, optional

        size: `int, optional

        compressed_dimension: `int`, optional

        count_variable: optional

        index_variable: optional

    :Returns:

         Ragged indexed contiguous array

        '''
        cls = self.get_class('RaggedIndexedContiguousArray')
        return cls(compressed_array=compressed_array, ndim=ndim,
                   shape=shape, size=size,
                   count_variable=count_variable,
                   index_variable=index_variable)

    def is_climatology(self, coordinate):
        '''Whether or not the coordinate represent climatologies.

    :Parameters:

        coordiante: coordinate construct

    :Returns:

        `bool`

        '''
        return bool(coordinate.get_geometry(None) == 'climatology')

    def is_field(self, construct):
        '''Return True if the construct is a field construct

    :Parameters:

        construct: Construct

    :Returns:

        `bool`

        '''
        return getattr(construct, 'construct_type', None) == 'field'

    def is_geometry(self, coordinate):
        '''Return True if the coordinate bounds are geometries.

    ..versionadded:: 1.8.0

    :Parameters:

        coordinate:
            The coordinate construct.

    :Returns:

        `bool`
             True if the coordinate bounds are geometries, otherwise
             False.

        '''
        return bool(coordinate.get_geometry(None) in (
            'point', 'line', 'polygon'))

    def is_masked(self, data):
        '''Whether or not the data has any masked values.

    .. versionadded:: 1.8.0

    :Parameters:

        data: `Data`

    :Returns:

        `bool`
            Whether or not the data has any masked values.

        '''
        return data.mask.any()

    def nc_set_instance_dimension(self, variable, ncdim):
        '''Set the netCDF instance dimension name.

    :Parameters:

        variable:

        ncdim: `str` or `None`
            The netCDF dimension name. If `None` then the name is not
            set.

    :Returns:

        `None`

        '''
        if ncdim is not None:
            variable.nc_set_instance_dimension(ncdim)

    def nc_set_sample_dimension(self, variable, ncdim):
        '''Set the netCDF sample dimension name.

    :Parameters:

        variable:

        ncdim: `str` or `None`
            The netCDF dimension name. If `None` then the name is not
            set.

    :Returns:

        `None`

        '''
        if ncdim is not None:
            variable.nc_set_sample_dimension(ncdim)

    def set_auxiliary_coordinate(self, field, construct, axes, copy=True):
        '''Insert a auxiliary coordinate object into a field.

    :Parameters:

        field: field construct

        construct: auxiliary coordinate construct

        axes: `tuple`

        copy: `bool`, optional

    :Returns:

        `str`

        '''
        return field.set_construct(construct, axes=axes, copy=copy)

    def set_bounds(self, construct, bounds, copy=True):
        '''Set the bounds component of a construct.

    :Parameters:

        construct: construct

        bounds: bounds component

        copy: `bool`, optional

    :Returns:

        `None`

        '''
        construct.set_bounds(bounds, copy=copy)

    def set_cell_measure(self, field, construct, axes, copy=True):
        '''Insert a cell_measure object into a field.

    .. versionadded:: 1.7.0

    :Parameters:

        field: field construct

        construct: cell measure construct

        axes: `tuple`

        copy: `bool`, optional

    :Returns:

        `str`

        '''
        return field.set_construct(construct, axes=axes, copy=copy)

    def set_cell_method(self, field, construct, copy=True):
        '''Insert a cell_method object into a field.

    .. versionadded:: 1.7.0

    :Parameters:

        field: field construct

        construct: cell method construct

        copy: `bool`, optional

    :Returns:

        `str`

        '''
        return field.set_construct(construct, copy=copy)

    def set_cell_method_axes(self, cell_method, axes):
        '''Set the axes of a cell method construct.

    :Parameters:

        construct: cell method construct

        axes:

    :Returns:

        `None`

        '''
        cell_method.set_axes(axes)

    def set_cell_method_method(self, cell_method, method):
        '''Set the method of a cell method construct.

    .. versionadded:: 1.7.0

    :Parameters:

        cell_method: cell method construct

        method: `str`

    :Returns:

        `None`

        '''
        cell_method.set_method(method)

    def set_coordinate_conversion(self, coordinate_reference,
                                  coordinate_conversion):
        '''Set the method of a cell method construct.

    .. versionadded:: 1.7.0

    :Parameters:

        coordinate_reference: coordinate reference construct

        coordinate_conversion: coordinate conversion component

    :Returns:

        `None`

        '''
        coordinate_reference.set_coordinate_conversion(coordinate_conversion)

    def set_coordinate_reference(self, field, construct, copy=True):
        '''Insert a coordinate reference object into a field.

    .. versionadded:: 1.7.0

    :Parameters:

        field: field construct

        construct: coordinate reference construct

        copy: `bool`, optional

    :Returns:

        `str`

        '''
        return field.set_construct(construct, copy=copy)

    def set_coordinate_reference_coordinates(self,
                                             coordinate_reference,
                                             coordinates):
        '''Set the coordinates of a coordinate reference construct.

    .. versionadded:: 1.7.0

    :Parameters:

        coordinate_reference: coordinate reference construct

        coordinates: sequence of `str`

    :Returns:

        `None`

        '''
        coordinate_reference.set_coordinates(coordinates)

    def set_coordinate_reference_coordinate(self,
                                            coordinate_reference,
                                            coordinate):
        '''Set a coordinate of a coordinate reference construct.

    :Parameters:

        coordinate_reference: coordinate reference construct

        coordinate: `str`

    :Returns:

        `None`

        '''
        coordinate_reference.set_coordinate(coordinate)

    def set_data(self, construct, data, axes=None, copy=True):
        '''The the data instance of a construct.

    :Parameters:

        construct: construct

        data: data instance

        axes: `tuple`, optional

        default: optional

    :Returns:

        `None`

        '''
        if axes is None:
            construct.set_data(data, copy=copy)
        else:
            construct.set_data(data, axes=axes, copy=copy)

    def set_datum(self, coordinate_reference, datum):
        '''Insert a datum object into a coordinate reference construct.

    :Parameters:

        coordinate_referece: coordinate reference construct

        datum: datum component

    :Returns:

        `None`

        '''
        coordinate_reference.set_datum(datum)

    def set_dimension_coordinate(self, field, construct, axes,
                                 copy=True):
        '''Insert a dimension coordinate object into a field.

    :Parameters:

        field: field construct

        construct: dimension coordinate construct

        axes: `tuple`

        copy: `bool`, optional

    :Returns:

        `str`

        '''
        return field.set_construct(construct, axes=axes, copy=copy)

    def set_domain_ancillary(self, field, construct, axes, copy=True):
        #                    extra_axes=0, copy=True):
        '''Insert a domain ancillary object into a field.

    :Parameters:

        field: field construct

        construct: domain ancillary construct`

        axes: `tuple`

        copy: `bool`, optional

    :Returns:

        `str`

        '''
        return field.set_construct(construct, axes=axes, copy=copy)

    def set_domain_axis(self, field, construct, copy=True):
        '''Insert a domain_axis object into a field.

    :Parameters:

        field: field construct

        construct: domain axis construct

        copy: `bool`, optional

    :Returns:

        `str`

        '''
        return field.set_construct(construct, copy=copy)

    def nc_set_external(self, construct):
        '''Set the external status of a construct.

    :Parameters:

        construct:

    :Returns:

        `None`

        '''
        construct.nc_set_external(True)

    def set_field_ancillary(self, field, construct, axes, copy=True):
        '''Insert a field ancillary object into a field.

    :Parameters:

        field: field construct`

        construct: field ancillary construct

        axes: `tuple`

        copy: `bool`, optional

    :Returns:

        `str`

        '''
        return field.set_construct(construct, axes=axes, copy=copy)

    def set_geometry(self, coordinate, value):
        '''Set the geometry type of a coordinate construct.

    .. versionadded:: 1.8.0

    :Parameters:

        coordinate: coordinate construct

        value: `str`

    :Returns:

        `None`

        '''
        coordinate.set_geometry(value)

    def set_inherited_properties(self, parent, inherited_properties,
                                 copy=True):
        '''Set any inherited properties.

    .. versionadded:: 1.8.6

    :Parameters:

        parent:
            The object that inherits the properties.

        inherited_properties: `dict`

        copy: `bool``

    :Returns:

        `None`

        '''
        parent.set_properties(inherited_properties, copy=copy)

    def set_node_count(self, parent, node_count, copy=True):
        '''Set a node count properties variable.

    .. versionadded:: 1.8.0

    :Parameters:

        parent:

        node_count: Node count properties variable

        copy: `bool`, optional

    :Returns:

        `None`
        '''
        parent.set_node_count(node_count, copy=copy)

    def set_part_node_count(self, parent, part_node_count, copy=True):
        '''Set a part node count properties variable.

    .. versionadded:: 1.8.0

    :Parameters:

        parent:

        part_node_count: part node count properties variable

        copy: `bool`, optional

    :Returns:

        `None`

        '''
        parent.set_part_node_count(part_node_count, copy=copy)

    def set_interior_ring(self, parent, interior_ring, copy=True):
        '''Insert an interior ring array into a coordiante.

    .. versionadded:: 1.8.0

    :Parameters:

        parent:

        interior_ring: interiot ring variable

        copy: `bool`, optional

    :Returns:

        `None`

    :Returns:

        `None`

        '''
        parent.set_interior_ring(interior_ring, copy=copy)

    def set_dataset_compliance(self, field, report):
        '''Set the dataset compliance report on a field construct.

    ..versionadded:: 1.7

    :Parameters:

        field: field construct

        report: `dict`

    :Returns:

        `None`

        '''
        field._set_dataset_compliance(report)

    def nc_set_dimension(self, construct, ncdim):
        '''Set the netCDF dimension name.

    :Parameters:

        construct: construct

        ncdim: `str` or `None`
            The netCDF dimension name. If `None` then the name is not
            set.

    :Returns:

        `None`

        '''
        if ncdim is not None:
            construct.nc_set_dimension(ncdim)

    def nc_set_geometry_variable(self, field, ncvar):
        '''Set the netCDF geometry container variable name.

    :Parameters:

        field: field construct

        ncvar: `str` or `None`
            The netCDF variable name. If `None` then the name is not
            set.

    :Returns:

        `None`

        '''
        if ncvar is not None:
            field.nc_set_geometry_variable(ncvar)

    def nc_set_variable(self, parent, ncvar):
        '''Set the netCDF variable name.

    :Parameters:

        parent:

        ncvar: `str` or `None`
            The netCDF variable name. If `None` then the name is not
            set.

    :Returns:

        `None`

        '''
        if ncvar is not None:
            parent.nc_set_variable(ncvar)

    def nc_get_datum_variable(self, ref):
        '''Get the netCDF grid mapping variable name for a datum.

    .. versionadded:: 1.7.5

    :Parameters:

        ref: Coordinate reference construct

    :Returns:

        `str` or `None`

        '''
        return ref.nc_get_datum_variable(default=None)

    def nc_set_datum_variable(self, ref, ncvar):
        '''Set the netCDF grid mapping variable name for a datum.

    .. versionadded:: 1.7.5

    :Parameters:

        ref: Coordinate reference construct

        ncvar: `str` or `None`
            The netCDF variable name. If `None` then the name is not
            set.

    :Returns:

        `None`

        '''
        if ncvar is not None:
            ref.nc_set_datum_variable(ncvar)

    def set_properties(self, construct, properties, copy=True):
        '''Set construct proporties.

    :Parameters:

        construct:

        properties: `dict`

        copy: `bool`

    :Returns:

        `None`

        '''
        construct.set_properties(properties, copy=copy)

    def has_bounds(self, construct):
        '''Whether or not a construct has bounds.

    :Parameters:

        construct:

    :Returns:

        `bool`

        '''
        return construct.has_bounds()

    def has_datum(self, coordinate_reference):
        '''Return True if a coordinate reference has a datum.

    :Parameters:

        coordinate_reference: coordinate reference construct

    :Returns:

        `bool`

    **Examples:**

    >>> if API.has_datum(ref):
    ...     print ref, 'has a datum'
    ... else:
    ...     print ref, 'does not have a datum'

        '''
        return bool(coordinate_reference.datum)

    def has_property(self, parent, prop):
        '''Return True if a property exists.

    :Parameters:

        parent:
            The object containing the property.

    :Returns:

        `bool`
            `True` if the property exists, otherwise `False`.

    **Examples:**

    >>> coord
    <DimensionCoordinate: latitude(180) degrees_north>
    >>> w.has_property(coord, 'units')
    True

    >>> bounds
    <Bounds: latitude(180, 2) degrees_north>
    >>> w.has_property(bounds, 'long_name')
    False
        '''
        return parent.has_property(prop)

    def squeeze(self, construct, axes=None):
        '''Remove size 1 axes from construct data.

    :Parameters:

        construct:

        axes: optional

    :Returns:

            The construct with removed axes.

        '''
        return construct.squeeze(axes=axes)

# --- End: class


_implementation = CFDMImplementation(
    cf_version=CF(),

    AuxiliaryCoordinate=AuxiliaryCoordinate,
    CellMeasure=CellMeasure,
    CellMethod=CellMethod,
    CoordinateReference=CoordinateReference,
    DimensionCoordinate=DimensionCoordinate,
    DomainAncillary=DomainAncillary,
    DomainAxis=DomainAxis,
    Field=Field,
    FieldAncillary=FieldAncillary,

    Bounds=Bounds,
    InteriorRing=InteriorRing,

    CoordinateConversion=CoordinateConversion,
    Datum=Datum,

    List=List,
    Index=Index,
    Count=Count,
    NodeCountProperties=NodeCountProperties,
    PartNodeCountProperties=PartNodeCountProperties,

    Data=Data,
    GatheredArray=GatheredArray,
    NetCDFArray=NetCDFArray,
    RaggedContiguousArray=RaggedContiguousArray,
    RaggedIndexedArray=RaggedIndexedArray,
    RaggedIndexedContiguousArray=RaggedIndexedContiguousArray,
)


def implementation():
    '''Return a container for the CF data model implementation.

    .. versionadded:: 1.7.0

    .. seealso:: `cfdm.example_field`, `cfdm.read`, `cfdm.write`

    :Returns:

        `CFDMImplementation`
            A container for the CF data model implementation.

    **Examples:**

    >>> i = cfdm.implementation()
    >>> i
    <CFDMImplementation: >
    >>> i.classes()
    {'AuxiliaryCoordinate': cfdm.auxiliarycoordinate.AuxiliaryCoordinate,
     'Bounds': cfdm.bounds.Bounds,
     'CellMeasure': cfdm.cellmeasure.CellMeasure,
     'CellMethod': cfdm.cellmethod.CellMethod,
     'CoordinateConversion': cfdm.coordinateconversion.CoordinateConversion,
     'CoordinateReference': cfdm.coordinatereference.CoordinateReference,
     'Count': cfdm.count.Count,
     'Data': cfdm.data.data.Data,
     'Datum': cfdm.datum.Datum,
     'DimensionCoordinate': cfdm.dimensioncoordinate.DimensionCoordinate,
     'DomainAncillary': cfdm.domainancillary.DomainAncillary,
     'DomainAxis': cfdm.domainaxis.DomainAxis,
     'Field': cfdm.field.Field,
     'FieldAncillary': cfdm.fieldancillary.FieldAncillary,
     'GatheredArray': cfdm.data.gatheredarray.GatheredArray,
     'Index': cfdm.index.Index,
     'InteriorRing': cfdm.interiorring.InteriorRing,
     'List': cfdm.list.List,
     'NetCDFArray': cfdm.data.netcdfarray.NetCDFArray,
     'NodeCountProperties': cfdm.nodecount.NodeCountProperties,
     'PartNodeCountProperties': cfdm.partnodecount.PartNodeCountProperties,
     'RaggedContiguousArray': cfdm.data.raggedcontiguousarray.RaggedContiguousArray,
     'RaggedIndexedArray': cfdm.data.raggedindexedarray.RaggedIndexedArray,
     'RaggedIndexedContiguousArray': cfdm.data.raggedindexedcontiguousarray.RaggedIndexedContiguousArray}

    '''
    return _implementation.copy()
