from enum import Enum
from .dotNETs import *


class DirectIoAccessObstacles(Enum):
    """This enum shows the obstacles which prevent the Direct IO access from taking place."""

    none = 0,
    """Direct I/O access is possible."""

    OldCompilerVersion = 1 << 0,
    """The compiler version is to old."""

    TargetSettingSeparateApplication = 1 << 1,
    """The symbol configuration is configured as a child object."""


class SymbolConfigContentFeatureFlags(Enum):
    """ The feature flags describing the contents of the symbol tables and XML files.
        (Introduced in V3.5.8.30, more broadly supported in V3.5.9.0.)

        Remark: The "runtime" part of this enum is also defined in the "ContentFeatureFlags" enumeration
        in the IecVarAccess Interfaces library.
    """

    none = 0,
    """Nothing configured."""

    MaskRuntime = 0xFFFF,
    """The runtime feature bit mask (also relevant for CRC calculation)."""

    MaskXml = 0xFFFF0000,
    """The XML feature bit mask (not relevant for CRC calculation)."""

    SupportOPCUA = 1,
    """Support OPC UA features (flag supported since V3.5.8.30). This is equal to the <see cref="ISymbolConfigObject6.SupportOPCUA"/> property.
        Remark: This is required for <see cref="IncludeComments"/>, <see cref="IncludeAttributes"/> and <see cref="IncludeTypeNodeAttributes"/>.
        In compiler versions V3.5.5.0 to V3.5.7.X, this implied <see cref="IncludeAttributes"/> with a filter matching only single IEC identifiers.
        In compiler versions V3.5.8.X, this implied <see cref="IncludeAttributes"/> with a filter matching IEC identifier pathes (e. G. foo.bar.baz).
    """

    IncludeComments = 2,
    """Include comments (flag supported since V3.5.9.0)."""

    IncludeAttributes = 4,
    """Include attributes (flag supported since V3.5.9.0)."""

    IncludeTypeNodeAttributes = 8,
    """Also include comments / attributes for type nodes (flag supported since V3.5.9.0)."""

    IncludeExecutables = 16,
    """ Inclusion of executable members (flag supported since V3.5.11.0, allows calling of programs, functions, FBs and methods, requires OPC UA).
        Remark: If this flag is set, the list of available signatures will also include callables.
    """

    UseEmptyNamespaceByDefault = 32,
    """ Assumes that effectively every POU has the {attribute 'namespace':=''} set.
        This is required to preserve compatibility to V2 symbol definitions.
    """

    XmlIncludeNodeFlags = 1 << 16,
    """ Include the node flags in the XML file (flag supported since V3.5.8.30).
        Remark: This was implied in compiler version V3.5.8.0, and is configurable using this
        flag since V3.5.8.30 due to backwards compatibility problems with various XML parsers.
    """

    XmlIncludeComments = 2 << 16,
    """ Include comments in the XML file (flag supported since V3.5.8.30), equal to <see cref="ISymbolConfigObject5.ExportCommentsInXML"/> flag.
        Remark: In compiler versions 3.5.5.X to 3.5.8.X, this implied <see cref="SymbolCommentFilterType.PreferDocuComments"/>.
    """

    XmlIncludeAttributes = 4 << 16,
    """Include the attributes in XML (flag supported since V3.5.9.0)."""

    XmlIncludeTypeNodeAttributes = 8 << 16,
    """Also include comments / attributes for type nodes (flag supported since V3.5.9.0)."""

    XmlIncludeExecutables = 16 << 16,
    """ Inclusion of executable members (flag supported since V3.5.11.0, allows calling of programs, functions, FBs and methods, requires OPC UA).
        Remark: This requires <see cref="IncludeExecutables"/> to be active - settingt his flag to false allows to suppress the executables in the for backwards compatibility.
    """


class SymbolAttributeFilterTypes(Enum):
    """Definition of the attribute matching type"""

    none = 0,
    """No attributes or not configured."""

    All = 1,
    """All attributes are included."""

    SimpleIdentifiers = 2,
    """ Match all simple identifiers without fullstop (non-hierarchical attributes).
        Remark: This is mainly here for backwards compatibility.
    """

    Prefix = 3,
    """Prefix matching of attributes"""

    Regex = 4,
    """Regex matching of attributes"""


class SymbolCommentFilterType(Enum):
    """Defines which comments are included in the XML file or symbol tables."""

    none = 0,
    """No comments are included at all, or not configured. """

    NormalComments = 1,
    """Only normal comments are included, those delimited with // or (* *)."""

    DocuComments = 2,
    """Only docu comments are included, those delimited with ///."""

    Both = 3,
    """ Include both normal and docu comments. This is the default, currently.
        Remark: This is equal to combining <see cref="NormalComments"/> and <see cref="DocuComments"/>.
    """

    PreferNormalComments = 4,
    """ Prefer the normal comments, docu comment is used when no normal comment is there.
        Remark: This implies <see cref="NormalComments"/> and <see cref="DocuComments"/>.
    """

    PreferDocuComments = 5,
    """ Prefer the docu comments, normal comment is used when docu comment is not there.
        Remark: This implies <see cref="NormalComments"/> and <see cref="DocuComments"/>.
    """


class ScriptSymbolConfigObjectMarker(object):
    """Every ScriptObject instance will be extended with this method.

    :version added: 3.5.10.0

    """

    @property
    def is_symbol_config(self):
        """Gets a value indicating whether this instance is a symbol config object.

        :rtype: bool
        :returns: ``True`` if this instance is symbol config object, otherwise ``False``.

        """
        pass


class ScriptSymbolConfigObject(ScriptSymbolConfigObjectMarker):
    """Functionality for manipulating symbol configuration objects.

    :version added: 3.5.10.0

    """

    @property
    def client_side_layout_calculator_guid(self):
        """Gets or sets the Guid denoting the currently configured client side layout calculator.

        Currently, two different values are allowed:
        ``Guid.Empty`` to use the Compatibility Offset Calculator which is always available.
        And "{0141eb75-141b-4ea1-9a8c-75f952b22a6c}" to use the OptimizedOutputOffsetCalculator
        which is new with V3.5.7.0 and also requires the compiler version 3.5.7.0
        (see http://jira.3s-software.com/browse/CDS-41816). This scheme may be extended to allow
        more or even arbitrary offset calculators in the future.

        :rtype: Guid

        """
        pass

    @client_side_layout_calculator_guid.setter
    def client_side_layout_calculator_guid(self, value: Guid):
        pass

    @property
    def client_side_layout_calculator(self):
        """Gets or sets the calculator object denoting the currently configured client side layout calculator.

        Currently, two different values are allowed:
        ``Guid.Empty`` to use the Compatibility Offset Calculator which is always available.
        And "{0141eb75-141b-4ea1-9a8c-75f952b22a6c}" to use the OptimizedOutputOffsetCalculator
        which is new with V3.5.7.0 and also requires the compiler version 3.5.7.0
        (see http://jira.3s-software.com/browse/CDS-41816). This scheme may be extended to allow
        more or even arbitrary offset calculators in the future.

        :rtype: :class:`ScriptClientSideLayoutCalculatorDescription`

        """
        pass

    @client_side_layout_calculator.setter
    def client_side_layout_calculator(self, value: ScriptClientSideLayoutCalculatorDescription):
        pass

    @property
    def available_client_side_layout_calculators(self):
        """Gets all currently known layout calculators.

        :rtype: :class:`ScriptClientSideLayoutCalculatorDescriptionCollection`

        """
        pass

    @property
    def enable_direct_io_access(self):
        """Gets or sets a boolean whether direct Access to the I/O Area is configured.

        Enabling direct access to the I/O area is supported for debugging
        purposes, e. G. testing the cables and connections. It is not meant for
        productive operation. It is only available under certain conditions, e. G.
        the compiler version must be >= V3.5.8.0 and the symbol config must not be
        generated as a child application.

        :rtype: bool

        """
        pass

    @enable_direct_io_access.setter
    def enable_direct_io_access(self, value: bool):
        pass

    def check_effective_direct_io_access(self):
        """Checks whether and why the direct Access to the I/O Area is effectively enabled / disabled.

        Enabling direct access to the I/O area is supported for debugging
        purposes, e. G. testing the cables and connections. It is not meant for
        productive operation. It is only available under certain conditions, e. G.
        the compiler version must be &gt;= V3.5.8.0 and the symbol config must not be
        generated as a child application.

        :rtype: :class:`DirectIoAccessObstacles`
        :returns: The :class:`DirectIoAccessObstacles` flag describing which
            reasons prevent the Direct IO Access from being enabled.

        """
        pass

    def get_direct_io_obstacle_explanations(self, obstacles):
        """Gets user readable, localized messages / explanations of the obstacles.

        :type obstacles: :class:`DirectIoAccessObstacles`
        :param obstacles: The obstacles.

        :rtype: list[str]
        :returns: A list of strings with one entry for each obstacle, or an "is enabled"
            message when ``obstacles`` == :attr:`DirectIoAccessObstacles.None`.

        """
        pass

    @property
    def content_feature_flags(self):
        """The configured content feature flags. This is partially redundant with :attr:`SymbolConfigObject.ExportCommentsInXML` and :attr:`SymbolConfigObject.SupportOPCUA`.

        :rtype: :class:`SymbolConfigContentFeatureFlags`

        """
        pass

    @content_feature_flags.setter
    def content_feature_flags(self, value: SymbolConfigContentFeatureFlags):
        pass

    @property
    def effective_content_feature_flags(self):
        """The effective content feature flags, considering the :attr:`content_feature_flags` and the compiler version setting.

        :rtype: :class:`SymbolConfigContentFeatureFlags`

        """
        pass

    def get_symbol_configuration_xsd(self):
        """Gets the current symbol configuration XML schema, as appropriate for the current symbol config object.

        The schema is delivered as a byte array, containing the UTF-8 encoded XSD file
        as it is also published in the http://www.3s-software.com/schemas/Symbolconfiguration.xsd.
        The above URL aways points to the newest released version of the schema, while
        the :meth:`get_symbol_configuration_xsd` property delivers the XSD file applicable
        to the current release of the SymbolConfig plugin.

        :rtype: list[byte]
        :returns: The current symbol configuration XML schema as byte array.

        """
        pass

    @property
    def symbol_attribute_filter_type(self):
        """The configured filter type for the attributes.

        :rtype: :class:`SymbolAttributeFilterTypes`

        """
        pass

    @symbol_attribute_filter_type.setter
    def symbol_attribute_filter_type(self, value: SymbolAttributeFilterTypes):
        pass

    @property
    def effective_symbol_attribute_filter_type(self):
        """The effective filter type, considering compiler version and other side conditions.

        :rtype: :class:`SymbolAttributeFilterTypes`

        """
        pass

    @property
    def symbol_attribute_filter_data(self):
        """Describes the filter data for :attr:`SymbolAttributeFilterTypes.Prefix` and :attr:`SymbolAttributeFilterTypes.Regex`.

        :rtype: str

        """
        pass

    @symbol_attribute_filter_data.setter
    def symbol_attribute_filter_data(self, value: str):
        pass

    @property
    def symbol_comment_filter_type(self):
        """The configured comment filter type.

        :rtype: :class:`SymbolCommentFilterType`

        """
        pass

    @symbol_comment_filter_type.setter
    def symbol_comment_filter_type(self, value: SymbolCommentFilterType):
        pass

    @property
    def effective_symbol_comment_filter_type(self):
        """The effective comment filter type, considering compiler version and other side conditions.

        :rtype: :class:`SymbolCommentFilterType`

        """
        pass

    def get_all_signatures(self, compile=True):
        """Get all signatures (compiler and configured).

        :type compile: bool
        :param compile: If True, build the application before generating the list. If the
            application was not built before, the returned list is empty.

        :rtype: :class:`ScriptSymbolConfigSignatureCollection`
        :returns: Collection of signatures.

        """
        pass

    def get_all_datatypes(self, compile=True):
        """Get all data types (compiler and configured).

        :type compile: bool
        :param compile: If True, build the application before generating the list. If the
            application was not built before, the returned list is empty.

        :rtype: :class:`ScriptSymbolConfigSignatureCollection`
        :returns: Collection of data types.

        """
        pass

    def get_only_configured_signatures(self):
        """Get only the configured signatures.

        :rtype: :class:`ScriptSymbolConfigSignatureCollection`
        :returns: Collection of signatures.

        """
        pass

    def get_only_configured_datatypes(self):
        """Get only the configured data types.

        :rtype: :class:`ScriptSymbolConfigSignatureCollection`
        :returns: Collection of data types.

        """
        pass


class ScriptClientSideLayoutCalculatorDescriptionCollection(list):
    """Descriptions of the client side layout calculators.

    :version added: 3.5.10.0

    """

    def __len__(self):
        """Gets the length (number of calculator descriptions).

        :rtype: int
        :returns: The number of calculator descriptions.

        """
        pass


class ScriptClientSideLayoutCalculatorDescription(object):
    """Description of an client side layout calculator.

    Currently, two different values are allowed:
    ``Guid.Empty`` to use the Compatibility Offset Calculator which is always available.
    And "{0141eb75-141b-4ea1-9a8c-75f952b22a6c}" to use the OptimizedOutputOffsetCalculator
    which is new with V3.5.7.0 and also requires the compiler version 3.5.7.0
    (see http://jira.3s-software.com/browse/CDS-41816). This scheme may be extended to allow
    more or even arbitrary offset calculators in the future.

    :version added: 3.5.10.0

    """

    @property
    def type_guid(self):
        """The unique ID of the output layout calculator.

        :rtype: Guid

        """
        pass

    @property
    def name(self):
        """The name of the output layout calculator - human readable and localized.

        :rtype: str

        """
        pass

    @property
    def description(self):
        """A longer description of the output layout calculator.

        :rtype: This may be shown in a tooltip, and should give some detailed
            explanation of the calculator, and e. G. the conditions under which the
            calculator is valid.

        """
        pass


class ScriptSymbolConfigSignature(object):
    """Signature element of the symbol configuration.

    :version added: 3.5.10.0

    """

    @property
    def name(self):
        """The name of this element.

        :rtype: str

        """
        pass

    @property
    def full_qualified_name(self):
        """The full qualified name of this element.

        :rtype: str

        """
        pass

    @property
    def library_id(self):
        """The identification of the library where this signature is declared.

        :rtype: str

        """
        pass

    @property
    def namespace_path(self):
        """Namespace path of the library where this signature is declared.

        :rtype: list <str>

        """
        pass

    @property
    def variables(self):
        """The variables of the signature.

        :rtype: :class:`ScriptSymbolConfigVariableCollection`

        """
        pass


class ScriptSymbolConfigSignatureCollection(list):
    """Collection of symbol configuration signatures.

    :version added: 3.5.10.0

    """

    def __len__(self):
        """Collection of symbol configuration signatures.

        :rtype: int
        :returns: The number of signatures.

        """
        pass

    def __getitem__(self, index_or_name):
        """Get the :class:`ScriptSymbolConfigSignature` at the specified position or the first :class:`ScriptSymbolConfigSignature` with the specified name which should be fully qualified.

        :type index_or_name: int or str
        :param index_or_name: Index of a element of the list or
            full qualified name of a signature. For example: Standard.TON

        :rtype: :class:`ScriptSymbolConfigSignature`
        :returns: Signature of the symbol configuration.

        """
        pass

    def find(self, name, library_id=None):
        """Get the first :class:`ScriptSymbolConfigSignature` with the specified name and library ID which should be fully qualified.

        :type name: str
        :param name: Name of a signature.

        :type library_id: str
        :param library_id: Library ID.

        :rtype: :class:`ScriptSymbolConfigSignature`
        :returns: Signature of the symbol configuration. Otherwise None.

        """
        pass


class ScriptSymbolConfigVariable(object):
    """Variable element of the symbol configuration.

    :version added: 3.5.10.0

    """

    @property
    def name(self):
        """The name of this variable.

        :rtype: str

        """
        pass

    @property
    def type(self):
        """The type of this variable, as the user declared it.

        :rtype: str

        """
        pass

    @property
    def comment(self):
        """Gets the comment of the signature or variable, or an empty string if no comment is available.

        This member is only valid for objects parsed from the compiler, not for configured
        symbol config instances.

        :rtype: str

        """
        pass

    @property
    def configured_access(self):
        """The allowed symbolic access to this variable.

        :rtype: :class:`SymbolAccess`

        """
        pass

    @configured_access.setter
    def configured_access(self, value):
        pass

    @property
    def maximal_access(self):
        """The maximal access that is allowed for this variable, decided by the given attributes.

        :rtype: :class:`SymbolAccess`

        """
        pass

    @property
    def effective_access(self):
        """The effective symbolic access to this variable.

        :rtype: :class:`SymbolAccess`

        """
        pass

    @property
    def exported_via_attribute(self):
        """Gets a value indicating whether this variable is configured via compiler attribute.

        :rtype: bool
        :returns: ``True`` if exported via attribute; otherwise ``False``. If ``True``, the Access
            attribute gives the effective access for this variable.

        """
        pass

    @property
    def attribute_access(self):
        """Gets the attribute access. When :attr:`attribute_access` is false, the result of this member is undefined.

        :rtype: :class:`SymbolAccess`

        """
        pass

    @property
    def type_library_id(self):
        """Gets the library id, when the type of the member is from a library.

        This is currently only set for supported data types (userdef and array).

        :rtype: str

        """
        pass

    @property
    def full_qualified_base_type(self):
        """Gets the full qualified base type of the member.

        This is currently only set for supported data types (userdef and array).

        :rtype: str

        """
        pass

    @property
    def alias_type(self):
        """The name of the alias type.

        For variables with aliased types, the Type, ``SymbolConfigVariable.VariableType``
        and ``SymbolConfigVariable2.FullQualifiedBaseType`` properties point to the effective,
        resolved type. Use this member in the UI to display the alias type used in the source.
        This member is only valid for objects parsed from the compiler, not for configured
        symbol config instances.

        :rtype: str

        """
        pass


class ScriptApplicationSymbolConfigExtension(object):
    """Extension provider for ApplicationObject instances.

    :version added: 3.5.10.0

    """

    def create_symbol_config(self, export_comments_to_xml, support_opc_ua,
                             client_side_layout_calculator):
        """Add the symbol configuration object to an application.

        :type export_comments_to_xml: bool

        :type support_opc_ua: bool

        :type client_side_layout_calculator: Guid

        :rtype: :class:`ScriptObject`
        :returns: Script object of the symbol config object.

        """
        pass


class ScriptSymbolConfigInvalidObjectException(Exception):
    """Exception which is thrown when the symbol configuration object is modified externally and so the scripting objects are not valid anymore.

    :version added: 3.5.10.0

    """

    def __init__(self, stMessage):
        """init."""
        pass
