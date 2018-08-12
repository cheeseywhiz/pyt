"""Control codes defined in ECMA-48"""
import enum

__all__ = 'C0', 'C1_7B', 'C1_8B', 'CSI'


class EnumMeta(enum.EnumMeta):
    def __contains__(self, value):
        return value in self._value2member_map_

    def __call__(self, value, names=None, **kwargs):
        if names is None and value not in self:
            return None
        else:
            return super().__call__(value, names=names, **kwargs)


class HexInt(int):
    def __repr__(self):
        return hex(self)


class HexIntEnum(HexInt, enum.Enum, metaclass=EnumMeta):
    pass


DEL = 0x7f


class C0(HexIntEnum):
    NUL = 0x00
    SOH = 0x01
    STX = 0x02
    ETX = 0x03
    EOT = 0x04
    ENQ = 0x05
    ACK = 0x06
    BEL = 0x07
    BS = 0x08
    HT = 0x09
    LF = 0x0a
    VT = 0x0b
    FF = 0x0c
    CR = 0x0d
    SO = 0x0e
    SI = 0x0f
    LS1 = 0x0e
    LS0 = 0x0f

    DLE = 0x10
    DC1 = 0x11
    DC2 = 0x12
    DC3 = 0x13
    DC4 = 0x14
    NAK = 0x15
    SYN = 0x16
    ETB = 0x17
    CAN = 0x18
    EM = 0x19
    SUB = 0x1a
    ESC = 0x1b
    IS4 = 0x1c
    IS3 = 0x1d
    IS2 = 0x1e
    IS1 = 0x1f


class C1_7B(HexIntEnum):
    # Set charset
    CS0 = 0x28  # (
    CS1 = 0x29  # )
    CS2 = 0x2a  # *
    CS3 = 0x2b  # +

    PAM = 0x3d  # =  # Application keypad
    PNM = 0x3e  # >  # Numeric keypad

    # 0x40  # @
    # 0x41  # A
    BPH = 0x42  # B
    NBH = 0x43  # C
    # 0x44  # D
    NEL = 0x45  # E
    SSA = 0x46  # F
    ESA = 0x47  # G
    HTS = 0x48  # H
    HTJ = 0x49  # I
    VTS = 0x4a  # J
    PLD = 0x4b  # K
    PLU = 0x4c  # L
    RI = 0x4d  # M
    SS2 = 0x4e  # N
    SS3 = 0x4f  # O

    DCS = 0x50  # P
    PU1 = 0x51  # Q
    PU2 = 0x52  # R
    STS = 0x53  # S
    CCH = 0x54  # T
    MW = 0x55  # U
    SPA = 0x56  # V
    EPA = 0x57  # W
    SOS = 0x58  # X
    # 0x59  # Y
    SCI = 0x5a  # Z
    CSI = 0x5b  # [
    ST = 0x5c  # \\
    OSC = 0x5d  # ]
    PM = 0x5e  # ^
    APC = 0x5f  # _

    RIS = 0x63  # c  # Reset


class C1_8B(HexIntEnum):
    # 0x80
    # 0x81
    BPH = 0x82
    NBH = 0x83
    # 0x84
    NEL = 0x85
    SSA = 0x86
    ESA = 0x87
    HTS = 0x88
    HTJ = 0x89
    VTS = 0x8a
    PLD = 0x8b
    PLU = 0x8c
    RI = 0x8d
    SS2 = 0x8e
    SS3 = 0x8f

    DCS = 0x90
    PU1 = 0x91
    PU2 = 0x92
    STS = 0x93
    CCH = 0x94
    MW = 0x95
    SPA = 0x96
    EPA = 0x97
    SOS = 0x98
    # 0x99
    SCI = 0x9a
    CSI = 0x9b
    ST = 0x9c
    OSC = 0x9d
    PM = 0x9e
    APC = 0x9f


class CSI(HexIntEnum):
    # Final Bytes of control sequences without Intermediate Bytes
    ICH = 0x40  # @
    CUU = 0x41  # A
    CUD = 0x42  # B
    CUF = 0x43  # C
    CUB = 0x44  # D
    CNL = 0x45  # E
    CPL = 0x46  # F
    CHA = 0x47  # G
    CUP = 0x48  # H
    CHT = 0x49  # I
    ED = 0x4a  # J
    EL = 0x4b  # K
    IL = 0x4c  # L
    DL = 0x4d  # M
    EF = 0x4e  # N
    EA = 0x4f  # O

    DCH = 0x50  # P
    SSE = 0x51  # Q
    CPR = 0x52  # R
    SU = 0x53  # S
    SD = 0x54  # T
    NP = 0x55  # U
    PP = 0x56  # V
    CTC = 0x57  # W
    ECH = 0x58  # X
    CVT = 0x59  # Y
    CBT = 0x5a  # Z
    SRS = 0x5b  # [
    PTX = 0x5c  # \\
    SDS = 0x5d  # ]
    SIMD = 0x5e  # ^
    # 0x5f  # _

    HPA = 0x60  # `
    HPR = 0x61  # a
    REP = 0x62  # b
    DA = 0x63  # c
    VPA = 0x64  # d
    VPR = 0x65  # e
    HVP = 0x66  # f
    TBC = 0x67  # g
    SM = 0x68  # h
    MC = 0x69  # i
    HPB = 0x6a  # j
    VPB = 0x6b  # k
    RM = 0x6c  # l
    SGR = 0x6d  # m
    DSR = 0x6e  # n
    DAQ = 0x6f  # o

    PRIV_0x70 = 0x70  # p
    PRIV_0x71 = 0x71  # q
    STBM = 0x72  # r  # Set Top and Bottom Margins
    PRIV_0x73 = 0x73  # s
    PRIV_0x74 = 0x74  # t
    PRIV_0x75 = 0x75  # u
    PRIV_0x76 = 0x76  # v
    PRIV_0x77 = 0x77  # w
    PRIV_0x78 = 0x78  # x
    PRIV_0x79 = 0x79  # y
    PRIV_0x7a = 0x7a  # z
    PRIV_0x7b = 0x7b  # {
    PRIV_0x7c = 0x7c  # |
    PRIV_0x7d = 0x7d  # }
    PRIV_0x7e = 0x7e  # ~
    PRIV_0x7f = 0x7f  # \x7f
