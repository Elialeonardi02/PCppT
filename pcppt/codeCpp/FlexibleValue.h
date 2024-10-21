class FlexibleValue {
public:
    int sizeString=100; //maximun dimension of string
    union Value {
        int i;
        float f;
        char c;
        bool b;
        short s;
        long long ll;
        unsigned char uc;
        unsigned short us;
        unsigned int ui;
        unsigned long long ull;
        double d;
        char str[100];

    } val;

    enum Type {
        INT,
        FLOAT,
        CHAR,
        BOOL,
        SHORT,
        LONG_LONG,
        UNSIGNED_CHAR,
        UNSIGNED_SHORT,
        UNSIGNED_INT,
        UNSIGNED_LONG_LONG,
        DOUBLE,
        STRING,
        UNKNOWN
    } currentType;

    FlexibleValue(int x) {
        this->val.i = x;
        currentType = INT;
    }

    FlexibleValue(float x) {
        this->val.f = x;
        currentType = FLOAT;
    }

    FlexibleValue(char x) {
        this->val.c = x;
        currentType = CHAR;
    }

    FlexibleValue(bool x) {
        this->val.b = x;
        currentType = BOOL;
    }

    FlexibleValue(short x) {
        this->val.s = x;
        currentType = SHORT;
    }

    FlexibleValue(long long x) {
        this->val.ll = x;
        currentType = LONG_LONG;
    }

    FlexibleValue(unsigned char x) {
        this->val.uc = x;
        currentType = UNSIGNED_CHAR;
    }

    FlexibleValue(unsigned short x) {
        this->val.us = x;
        currentType = UNSIGNED_SHORT;
    }

    FlexibleValue(unsigned int x) {
        this->val.ui = x;
        currentType = UNSIGNED_INT;
    }

    FlexibleValue(unsigned long long x) {
        this->val.ull = x;
        currentType = UNSIGNED_LONG_LONG;
    }

    FlexibleValue(double x) {
        this->val.d = x;
        currentType = DOUBLE;
    }

    FlexibleValue(const char* x) {
        for (int i = 0; i < this->sizeString-1 && x[i] != '\0'; i++) {
            val.str[i] = x[i];
        }
        val.str[this->sizeString-1] = '\0';
        currentType = STRING;
    }

    void setValue(int x) {
        if (currentType == INT) {
            val.i = x;
        }
    }

    void setValue(float x) {
        if (currentType == FLOAT) {
            val.f = x;
        }
    }

    void setValue(char x) {
        if (currentType == CHAR) {
            val.c = x;
        }
    }

    void setValue(bool x) {
        if (currentType == BOOL) {
            val.b = x;
        }
    }

    void setValue(short x) {
        if (currentType == SHORT) {
            val.s = x;
        }
    }

    void setValue(long long x) {
        if (currentType == LONG_LONG) {
            val.ll = x;
        }
    }

    void setValue(unsigned char x) {
        if (currentType == UNSIGNED_CHAR) {
            val.uc = x;
        }
    }

    void setValue(unsigned short x) {
        if (currentType == UNSIGNED_SHORT) {
            val.us = x;
        }
    }

    void setValue(unsigned int x) {
        if (currentType == UNSIGNED_INT) {
            val.ui = x;
        }
    }

    void setValue(unsigned long long x) {
        if (currentType == UNSIGNED_LONG_LONG) {
            val.ull = x;
        }
    }

    void setValue(double x) {
        if (currentType == DOUBLE) {
            val.d = x;
        }
    }

    void setValue(const char* x) {
        if (currentType == STRING) {
            for (int i = 0; i < this->sizeString-1 && x[i] != '\0'; i++) {
                val.str[i] = x[i];
            }
            val.str[this->sizeString-1] = '\0';
        }
    }

    void assignValue(int &x) {
        if (currentType == INT) {
            x = val.i;
        }
    }

    void assignValue(float &x) {
        if (currentType == FLOAT) {
            x = val.f;
        }
    }

    void assignValue(char &x) {
        if (currentType == CHAR) {
            x = val.c;
        }
    }

    void assignValue(bool &x) {
        if (currentType == BOOL) {
            x = val.b;
        }
    }

    void assignValue(short &x) {
        if (currentType == SHORT) {
            x = val.s;
        }
    }

    void assignValue(long long &x) {
        if (currentType == LONG_LONG) {
            x = val.ll;
        }
    }

    void assignValue(unsigned char &x) {
        if (currentType == UNSIGNED_CHAR) {
            x = val.uc;
        }
    }

    void assignValue(unsigned short &x) {
        if (currentType == UNSIGNED_SHORT) {
            x = val.us;
        }
    }

    void assignValue(unsigned int &x) {
        if (currentType == UNSIGNED_INT) {
            x = val.ui;
        }
    }

    void assignValue(unsigned long long &x) {
        if (currentType == UNSIGNED_LONG_LONG) {
            x = val.ull;
        }
    }

    void assignValue(double &x) {
        if (currentType == DOUBLE) {
            x = val.d;
        }
    }

    void assignValue(char* x) {
        if (currentType == STRING) {
            for (int i = 0; i < this->sizeString; i++) {
                x[i] = val.str[i];
            }
        }
    }

    bool compare(const auto& pred) {
        switch (currentType) {
            case INT:
                return pred(val.i);
            case FLOAT:
                return pred(val.f);
            case CHAR:
                return pred(val.c);
            case BOOL:
                return pred(val.b);
            case SHORT:
                return pred(val.s);
            case LONG_LONG:
                return pred(val.ll);
            case UNSIGNED_CHAR:
                return pred(val.uc);
            case UNSIGNED_SHORT:
                return pred(val.us);
            case UNSIGNED_INT:
                return pred(val.ui);
            case UNSIGNED_LONG_LONG:
                return pred(val.ull);
            case DOUBLE:
                return pred(val.d);
            case STRING:
                for (int i = 0; i<this->sizeString ; i++) {
                    if (not pred(val.str[i]))
                        return false;
                    if (val.str[i] == '\0') {
                        break;
                    }
                }
                return true;
            default:
                return false;
        }
    }
};
