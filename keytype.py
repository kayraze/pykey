from enum import Enum, auto

class KeyType(Enum):
    ESC = auto()
    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()
    
    TILDE = auto()
    NUM_1 = auto()
    NUM_2 = auto()
    NUM_3 = auto()
    NUM_4 = auto()
    NUM_5 = auto()
    NUM_6 = auto()
    NUM_7 = auto()
    NUM_8 = auto()
    NUM_9 = auto()
    NUM_0 = auto()
    
    MINUS = auto()
    EQUALS = auto()
    BACKSPACE = auto()
    TAB = auto()
    
    Q = auto()
    W = auto()
    E = auto()
    R = auto()
    T = auto()
    Y = auto()
    U = auto()
    I = auto()
    O = auto()
    P = auto()
    
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    BACKSLASH = auto()
    
    A = auto()
    S = auto()
    D = auto()
    F = auto()
    G = auto()
    H = auto()
    J = auto()
    K = auto()
    L = auto()
    
    SEMICOLON = auto()
    APOSTROPHE = auto()
    ENTER = auto()
    
    LEFT_SHIFT = auto()
    Z = auto()
    X = auto()
    C = auto()
    V = auto()
    B = auto()
    N = auto()
    M = auto()
    
    COMMA = auto()
    PERIOD = auto()
    SLASH = auto()
    RIGHT_SHIFT = auto()
    
    CONTROL = auto()
    WINDOWS = auto()
    ALT = auto()
    
    SPACE = auto()
    
    CAPS_LOCK = auto()
    F13 = auto()  # For keyboards with additional function keys
    F14 = auto()
    F15 = auto()
    
    LEFT_ARROW = auto()
    UP_ARROW = auto()
    RIGHT_ARROW = auto()
    DOWN_ARROW = auto()
    
    INSERT = auto()
    HOME = auto()
    PAGE_UP = auto()
    DELETE = auto()
    END = auto()
    PAGE_DOWN = auto()
    
    NUM_LOCK = auto()
    NUMPAD_0 = auto()
    NUMPAD_1 = auto()
    NUMPAD_2 = auto()
    NUMPAD_3 = auto()
    NUMPAD_4 = auto()
    NUMPAD_5 = auto()
    NUMPAD_6 = auto()
    NUMPAD_7 = auto()
    NUMPAD_8 = auto()
    NUMPAD_9 = auto()
    
    NUMPAD_ENTER = auto()
    NUMPAD_PLUS = auto()
    NUMPAD_MINUS = auto()
    NUMPAD_MULTIPLY = auto()
    NUMPAD_DIVIDE = auto()

    # Special keys
    HOSTKEY = auto()
    PRINT_SCREEN = auto()
    SCROLL_LOCK = auto()
    PAUSE = auto()