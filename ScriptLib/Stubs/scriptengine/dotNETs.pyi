from enum import Enum


class Guid(object):
    """.Net's type System.Guid"""

    @property
    def Empty(self):
        """Empty Guid.

        :rtype: Guid

        """
        pass


class Version(object):
    """.Net#s type System.Version"""

    def Revision(self) -> int:
        pass

    def Revision(self) -> int:
        pass

    def Build(self) -> int:
        pass

    def Minor(self) -> int:
        pass

    def Major(self) -> int:
        pass

    def MinorRevision(self) -> int:
        pass

    def MajorRevision(self) -> int:
        pass

    def ToString(self) -> str:
        pass


class IPAddress(object):
    """.Net's type System.Net.IPAddress"""
    pass


class DateTime(object):
    """.Net's type System.DateTime"""


class TimeSpan(object):
    """.Net's type System.TimeSpan"""

    def ToString(self) -> str:
        pass


class Color(object):
    """.Net's type System.Drawing.Color"""
    pass


class Icon(object):
    """.Net's type System.Drawing.Icon"""
    pass


class Image(object):
    """.Net's type System.Drawing.Image"""
    pass


class Stream(object):
    """.Net's System.IO.Stream"""
    pass


class Uri(object):
    """.Net's System.Uri"""
    pass


class XmlElement(object):
    """.Net's System.Xml.XmlElement"""
    pass


class XmlWriter(object):
    """.Net's System.Xml.XmlWriter"""
    pass


class X509Certificate2(object):
    """.Net's System.Security.Cryptography.X509Certificates.X509Certificate2"""
    pass


class X509Chain(object):
    """.Net's System.Security.Cryptography.X509Certificates.X509Chain"""
    pass


class Win32Window(object):
    """.Net's System.Windows.Forms.IWin32Window"""
    pass


class EventArgs(object):
    """.Net's System.EventArgs """
    pass


class CancelEventArgs(EventArgs):
    """.Net's System.ComponentModel.CancelEventArgs"""
    pass


class HandledEventArgs(EventArgs):
    """.Net's System.ComponentModel.HandledEventArgs"""
    pass


class DialogResult(Enum):
    """System.Windows.Forms.DialogResult"""
    None = 0
    OK = 1
    Cancel = 2
    Abort = 3
    Retry = 4
    Ignore = 5
    Yes = 6
    No = 7


class PSNode(object):
    """_3S.CoDeSys.Core.Objects.IPSNode"""
    pass


class ProgressCallback(object):
    """_3S.CoDeSys.Core.IProgressCallback"""
    pass


class ProjectStructure(object):
    """_3S.CoDeSys.Core.Objects.IProjectStructure4"""
    pass


class RcsSelectionVerificationArgs(object):
    """_3S.CoDeSys.RevisionControlHooks.RcsSelectionVerificationArgs"""
    pass


class RcsVirtualProject(object):
    """_3S.CoDeSys.RevisionControlHooks.IRcsVirtualProject"""
    pass


class RcsVirtualProjectNode(object):
    """_3S.CoDeSys.RevisionControlHooks.RcsVirtualProjectNode"""
    pass

