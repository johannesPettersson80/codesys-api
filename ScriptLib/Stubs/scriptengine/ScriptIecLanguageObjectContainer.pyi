from enum import Enum
from .dotNETs import *
from .ScriptObject import *


class PouType(Enum):
    """Defines the type of the POU which is to be created.

    :version added: 3.5.9.0

    """

    Program = 1
    """A Program."""

    FunctionBlock = 2
    """A function block."""

    Function = 3
    """A function."""


class DutType(Enum):
    """Defines the type of the DUT which is to be created.

    :version added: 3.5.9.0

    """

    Structure = 1
    """A structure."""

    Enumeration = 2
    """An enumeration."""

    Alias = 3
    """An alias."""

    Union = 4
    """A union."""

    EnumerationWithTextList = 5
    """An enumeration with integrated text list support."""


class SpecialPouType(Enum):
    """Defines the type of special POUs (with implicit checks) which have to be created.

    :version added: 3.5.12.10

    """

    none = 1
    """No special POU."""

    check_bounds = 2
    """Bound checks.
    
    Appropriate handling of bound violations; such handling includes setting flags or changing field indices.
    
    """

    check_pointer = 3
    """Pointer checks."""

    check_range_unsigned = 4
    """Check range unsigned."""

    check_range_signed = 5
    """Check range signed."""

    check_div_real_64 = 6
    """Check division real 64 bit."""

    check_div_real_32 = 7
    """Check division real 32 bit."""

    check_div_int_64 = 8
    """Check division real 64 bit."""

    check_div_int_32 = 9
    """Check division real 32 bit."""

    check_l_range_unsigned = 10
    """L-range checks unsigned."""

    check_l_range_signed = 11
    """L-range checks signed."""


class ScriptIecLanguageObjectContainer(object):
    """This allows objects to create POU like objects, the methods will be available in the project root as well as applications, and folders below them.

    The extended settings and specializations which are available in the "Add Object" dialog, but
    not available in this interface, can be implemented by direct access of the textual declaration
    part via :class:`ScriptObjectWithTextualDeclaration` - for example, setting derived interfaces,
    or persistent or constant GVLs.

    :version added: 3.5.9.0

    """

    def create_pou(self, name: str, type: PouType = PouType.FunctionBlock, language: Guid = None,
                   return_type: str = None, base_type: str = None, interfaces: str = None):
        """
        Creates a POU with the specified name and type.

        .. warning:: The original C# function that is called with this method contains 2 overloads.
            It is strongly advised to pass *all* arguments with their respective keywords.

        :type name: str
        :param name: The name.

        :type type: :class:`PouType`
        :param type: The type. Optional, the default is a function block.

        :type language: Guid
        :param language: The language. Optional, the default is structured text.

        :type return_type: str
        :param return_type: The return type. This is required for
            :attr:`PouType.Function`, and not allowed for other POU types.

        :type base_type: str
        :param base_type: The base type.
            This is optional and only allowed for :attr:`PouType.FunctionBlock`.

        :type interfaces: str
        :param interfaces: The implemented interface(s).
            This is optional and only allowed for :attr:`PouType.FunctionBlock`.

        :raises Exception: Any exception which might occur (e. G. if the name is not an IEC
            identifier, or an object with the same name already exists within the same namespace,
            or the language guid is not valid, or the object cannot be created under this parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created POU.

        """
        pass

    def create_pou(self, type: SpecialPouType):
        """
        Creates a POU with implicit checks according to the specified type.

        Adding a check function will provoke a full recompile and prohibit an online change.

        :version added: 3.5.12.10

        :type type: :class:`SpecialPouType`
        :param type: The :class:`SpecialPouType` which should be created.

        :raises Exception: Any exception which might occur (e. G. if an object with the same name
            already exists within the same namespace or the object cannot be created under this
            parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created POU.

        """
        pass

    def create_gvl(self, name):
        """Creates a GVL with the specified name.

        :type name: str
        :param name: The name.

        :raises Exception: Any exception which might occur (e. G. if the name is not an IEC
            identifier, or an object with the same name already exists within the same namespace,
            or the language guid is not valid, or the object cannot be created under this parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created GVL.

        """
        pass

    def create_dut(self, name, type=DutType.Structure, baseType=None):
        """Creates a DUT with the specified name and type.

        As with manual object creation in the UI, enums will get the attribute 'strict' with
        compiler versions >= 3.5.7.0, and additionally the attribute 'qualified_only' with
        compiler version 3.5.8.0.

        :type name: str
        :param name: The name.

        :type type: :class:`DutType`
        :param type: The type.

        :type baseType: str
        :param baseType: The base type. This optional parameter is necessary for for Alias types,
            optional for STRUCTs and enums, and currently not allowed for unions.

        :raises Exception: Any exception which might occur (e. G. if the name is not an IEC
            identifier, or an object with the same name already exists within the same namespace,
            or the language guid is not valid, or the object cannot be created under this parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created DUT.

        """
        pass

    def create_interface(self, name, baseInterfaces="__System.IQueryInterface"):
        """Creates an interface with the specified name.

        :type name: str
        :param name: The name.

        :type baseInterfaces: str
        :param baseInterfaces: The base interfaces (comma separated).

        :raises Exception: Any exception which might occur (e. G. if the name is not an IEC
            identifier, or an object with the same name already exists within the same namespace,
            or the language guid is not valid, or the object cannot be created under this parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created interface.

        """
        pass

    def create_persistentvars(self, name):
        """Creates a persistent GVL with the specified name.

        :type name: str
        :param name: The name.

        :raises Exception: Any exception which might occur (e. G. if the name is not an IEC
            identifier, or an object with the same name already exists within the same namespace,
            or the language guid is not valid, or the object cannot be created under this parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created persistent GVL.

        """
        pass


class ScriptIecLanguageMemberContainer(object):
    """This allows objects to create POU like member objects, the methods will be available on POUs, Interfaces, GVLs, and folders below them.

    The extended settings and specializations which are available in the "Add Object" dialog, but
    not available in this interface, can be implemented by direct access of the textual declaration
    part via :class:`ScriptObjectWithTextualDeclaration` - for example, setting derived interfaces,
    or persistent or constant GVLs.

    :version added: 3.5.9.0

    See also: :class:`ScriptTreeObject`

    """

    def create_property(self, name, return_type="int", language=None):
        """Creates a property with the specified name and type.

        :type name: str
        :param name: The name.

        :type return_type: str
        :param return_type: The return type.

        :type language: Guid or None
        :param language: The language for the getter and setter. Optional, the default is
            structured text. It is illegal to specify a language for interface properties.

        :raises Exception: Any exception which might occur (e. G. if the name is not an IEC
            identifier, or an object with the same name already exists within the same namespace,
            or the language guid is not valid, or the object cannot be created under this parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created property.

        """
        pass

    def create_method(self, name, return_type=None, language=None):
        """Creates a method with the specified name and type.

        Methods cannot be added to GVLs or Functions.

        :type name: str
        :param name: The name.

        :type return_type: str
        :param return_type: The return type.

        :type language: Guid or None
        :param language: The language for the getter and setter.
            Optional, the default is structured text.

        :raises Exception: Any exception which might occur (e. G. if the name is not an IEC
            identifier, or an object with the same name already exists within the same namespace,
            or the language guid is not valid, or the object cannot be created under this parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created method.

        """
        pass

    def create_action(self, name, language=None):
        """Creates an action with the specified name and type.

        Actions cannot be added to GVLs or Functions.

        :type name: str
        :param name: The name.

        :type language: Guid or None
        :param language: The language for the getter and setter.
            Optional, the default is structured text.

        :raises Exception: Any exception which might occur (e. G. if the name is not an IEC
            identifier, or an object with the same name already exists within the same namespace,
            or the language guid is not valid, or the object cannot be created under this parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created action.

        """
        pass

    def create_transition(self, name, language=None):
        """Creates an transition with the specified name and type.

        Transitions cannot be added to GVLs or Functions.

        :type name: str
        :param name: The name.

        :type language: Guid or None
        :param language: The language for the getter and setter.
            Optional, the default is structured text.

        :raises Exception: Any exception which might occur (e. G. if the name is not an IEC
            identifier, or an object with the same name already exists within the same namespace,
            or the language guid is not valid, or the object cannot be created under this parent.

        :rtype: :class:`ScriptObject`
        :returns: The ScriptObject of the newly created transition.

        """
        pass


class ScriptImplementationLanguage(object):
    """Defines the Guids for the standard IEC 61131-3 languages and those available as CODESYS extensions.

    An instance of this interface will be injected with the name
    "ImplementationLanguages".

    :version added: 3.5.9.0

    """

    @property
    def st(self):
        """Gets the language guid for ST / Structured Text.

        :rtype: Guid

        """
        pass

    @property
    def cfc(self):
        """Gets the language guid for CFC / Continous Flow Chart (free layout FUP).

        :rtype: Guid

        """
        pass

    @property
    def page_oriented_cfc(self):
        """Gets the language guid for Page oriented CFC / Continous Flow Chart (free layout FUP).

        :rtype: Guid

        """
        pass

    @property
    def fbd(self):
        """Gets the language guid for FBD / Function Block Diagram (FBS).

        :rtype: Guid

        """
        pass

    @property
    def instruction_list(self):
        """Gets the language guid for IL / Instruction List (AWL).

        :rtype: Guid

        """
        pass

    @property
    def ladder(self):
        """Gets the language guid for LD / Ladder Diagram (KOP).

        :rtype: Guid

        """
        pass

    @property
    def sfc(self):
        """Gets the language guid for SFC / Secuential Function Chart (AS).

        Currently, SFC cannot be used for
        :meth:`ScriptIecLanguageObjectContainer.create_pou`
        with :attr:`PouType.Function`,
        :meth:`ScriptIecLanguageMemberContainer.create_method`,
        :meth:`ScriptIecLanguageMemberContainer.create_property`
        and :meth:`ScriptIecLanguageMemberContainer.create_transition`.

        :rtype: Guid

        """
        pass

    @property
    def uml_statechart(self):
        """Gets the language guid for the uml statechart.

        The UML AddOn needs to be installed for this language.
        See also: http://store.codesys.com/codesys-uml.html

        :rtype: Guid

        """
        pass
