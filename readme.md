# Tipi supportati

| **Python** | **cpp** |
| --- | --- |
| None | void |
| int | int |
| float | float |
| bool | bool |
| int8 | char |
| int16 | short |
| int32 | int |
| int64 | long long |
| uint8 | unsigned char |
| uint16 | unsigned short |
| uint32  | unsigned int |
| uint64 | unsigned long long |
| float16 | half |
| float32  | float  |
| float64 | double |
| str | char |

I tipi `int8`, `int16`, `int32`, `uint8`, `uint16`, `uint32`, `uint64`, `float16`, `float32`, `float64` non sono nativamente supportati dall'interprete Python. Per eseguire anche il codice Python, è necessario assegnare a questi tipi uno equivalente supportato dall'interprete. Le assegnazioni nel root scope verranno ignorate dal parser.

```python
int64=int
a:int64=1
```

```cpp
long long a=1
```

# Statment

## FunctionDef

Parsing di una funzione o metodo a appartenente ad una classe, in tutte e due casi è possibile specificare le seguenti informazioni riguardati la firma della funzione o del metodo>

**Arguments:** se un tipo di un parametro non è specificato nella firma, viene assegnata la keyword `auto`.

```python
def fun(a)->int:
	return a=a+1
```

```cpp
int fun(auto a){
	return a=a+1;
}
```

**Return**: se il tipo di ritorno della funzione non è specificato, la dichiarazione C++ utilizzerà un costrutto `template` per una dichiarazione generica.

```python
def fun(v):
    return v
```

```cpp
template<typename T>
T fun(v) {
    return v; 
}
```

Nel caso in cui venga definite due funzioni annidate, nella traduzione C++ le due funzioni verranno separate

```python
def out_function(a:int)->int:
    return a
    def inner_function()->int:
        return 2
```

```cpp
int inner_function()
{
  return 2;
}

int outer_function(int a)
{
    return a;
}

```

Invece esclusivamente per i metodi delle classi vengono applicati i seguenti comportamenti: 

- Viene rimosso l’attributo `self` dalla firma.
- Il metodo `__init__` viene tradotto nella rispettiva versione del costruttore di classe C++ avente il medesimo nome della classe.

```python
class test:
    def __init__(self):
        self.a=1
```

```cpp
class test{
public:
  int a;

  test() 
  {
    this->a = 1;
  }

};
```

## ClassDef

Parsing di classi, è possibile metodi e attributi specificandone anche la visibilità rispettando la seguente sintassi:

`<name>`: visibilità pubblica.

`_<name>`: visibilità protected.

`__<name>`: visibilità private.

```python
class test:
    a:int
    _b:float
    __c:int
    def __init__(self):
        self.a=1
    def a_plus_c(self)->int:
        return self.a+self._b
```

```cpp
class test{
protected:
  float _b;

private:
  int __c;

public:
  int a;

  test() 
  {
    this->a = 1;
  }

  int a_plus_c() 
  {
    return this->a + this->_b;
  }

};
```

La destrutturazione sugli attributi produrrà istruzioni multiple sugli attributi coinvolti:

```python
class test:
    def __init__(self):
        self.d,self.c=1
        self.d+=1
        self.c=self.d*2
```

```cpp
class test{
public:
  int d;

  int c;

  test() 
  {
    this->d = 1;
    this->c = 1;
    this->d += 1;
    this->c = this->d * 2;
  }

};

```

Il parsing di classi composte solo esclusivamente da membri pubblici produrrà una struct c++

```python
class test:
    a:int
    b:float=0.2

```

```cpp
struct test{
public:
  int a;

  float b = 0.2;

};
```

## Assign

Parsing assegnazioni.

**Attribute:** parsing delle operazioni sugli attributi all’interno dei metodi di una classe: 

- Gli attributi dichiarati come `self.<name>` in Python saranno tradotti in `this-><name>` in C++.
    
    
    ```python
    class test{
    public:
      int a = 1;
    
      test() 
      {
        this->a = 1;
      }
    
    };
    ```
    
    ```cpp
    class test{
    public:
      int a = 1;
    
      test() 
      {
        this->a = 1;
      }
    
    };
    ```
    
- Nel caso in cui l’attributo non sia presente all’interno della classe, ne verrà aggiunta la dichiarazione come attributo della classe, come in una comune dichiarazione dell’attributo, la [visibilità](https://www.notion.so/Funzionalit-supportate-135e8d35bc1f800aa17ade39302b716b?pvs=21) è data dal nome dell’attributo.
    
    
    ```cpp
    class test:
        def __init__(self):
            self.a=1
    ```
    
    ```cpp
    class test{
    public:
      int a = 1;
    
      test() 
      {
        this->a = 1;
      }
    
    };
    ```
    

**Lambda:** è possibile dichiarare lambda function nella forma `<name> = lambda <parametro> : <espressione>`. In C++ si utilizzeranno le deduzioni di tipo del compilatore.

```python
def test()->None:
    lm= lambda x: x * 2

```

```cpp
void test();

void test()
{
  auto lm = [](auto x) {x * 2;};
}
```

La destrutturazione sulle dichiarazioni di lambda functions produrrà istruzioni multiple, una per ogni variabile specificata come target:

```python
def test()->None:
    lm,cm,cd= lambda x: x * 2
```

```cpp
void test();

void test()
{
  auto lm = [](auto x) {x * 2;};
  auto cm = [](auto x) {x * 2;};
  auto cd = [](auto x) {x * 2;};
}
```

**Variabili:** È possibile accedere ed assegnare valori a variabili di [tipi supportati](https://www.notion.so/Funzionalit-supportate-135e8d35bc1f800aa17ade39302b716b?pvs=21).

- Nel caso in cui una variabile non sia stata definita, verrà aggiunta la rispettiva dichiarazione, deducendo il tipo dall’espressione, nel caso in cui non sia possibile, verrà lasciato il compito di dedurre il tipo al compilatore C++ `auto`
    
    
    ```python
    def test()->None:
        b:float
        a=0.1
        b=a+1
    ```
    
    ```cpp
    void test();
    
    void test()
    {
      float b;
      float a = 0.1;
      b = a + 1;
    }
    ```
    
- La destrutturazione su più variabili produrrà istruzioni multiple, una per ogni variabile introdotta:
    
    
    ```python
    def test()->None:
        a,b=0.3
    ```
    
    ```cpp
    void test();
    
    void test()
    {
      float a = 0.3;
      float b = 0.3;
    }
    
    ```
    

**Array**: è possibile accedere e assegnare valori agli elementi di un array dei [tipi supportati](https://www.notion.so/Funzionalit-supportate-135e8d35bc1f800aa17ade39302b716b?pvs=21).

- Nel caso in cui un’array non sia stato definito, verrà aggiunta la rispettiva dichiarazione, deducendo il tipo dall’espressione, nel caso in cui non sia possibile, verrà lasciato il compito di dedurre il tipo al compilatore C++ `auto`
    
    
    ```python
    def test()->None:
        c:[int]=[4,5,6]
        a=[1,2,3]
        a[0]=c[1]*4
    ```
    
    ```cpp
    void test();
    
    void test()
    {
      int c[] = {4, 5, 6};
      int a[3] = {1, 2, 3};
      a[0] = c[1] * 4;
    }
    ```
    
- Per ri-assegnare un array esistente con una nuova lista, viene creato un array temporaneo e assegnato elemento per elemento.
    
    
    ```python
    def test()->None:
        a=[1,2,3,4,5,6]
        a=[6,7,8,9,10,11]
    ```
    
    ```cpp
    void test();
    
    void test()
    {
      int a[6] = {1, 2, 3, 4, 5, 6};
      {
        int temp_array_assign[6] = {6, 7, 8, 9, 10, 11};
        for (int i=0; i<6; i++) {
          a[i] = temp_array_assign[i];
        }
      }
    }
    ```
    
- La destrutturazione su più array produrrà istruzioni multiple, una per ogni array introdotto:
    
    
    ```python
    def test()->None:
        a,b=[1,2,3,4,5,6]
    ```
    
    ```cpp
    void test();
    
    void test()
    {
      int a[6] = {1, 2, 3, 4, 5, 6};
      int b[6] = {1, 2, 3, 4, 5, 6};
    }
    ```
    

## AnnAssign

**Variabili:** È specificare un'annotazione di tipo (type hints) in modo da dichiarare il tipo della variabile durante la sua inizializzazione `<name>:<type>=<expr>`, `<expr>` è opzionale

```python
def test()->None:
    a:int
```

```cpp
void test();

void test()
{
  int a;
}

```

**Array:** È possibile dichiarare anche gli array `<name>:[<type>]=<expr>`, oppure specificando la dimensione `<name>:[<type>,<dim>]=<expr>`, `<expr>` è opzionale

```python
def test()->None:
    c:[int]=[5,6,7]
    a:[int,10]=[1,2]
    a[3]=c[1]+a[1]
```

```cpp
void test();

void test()
{
  int c[] = {5, 6, 7};
  int a[10] = {1, 2};
  a[3] = c[1] + a[1];
}
```