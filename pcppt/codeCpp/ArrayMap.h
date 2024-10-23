template <typename K, typename V>
struct KeyValuePair {
    K key;
    V value;

    KeyValuePair() : key(K()), value(V()) {}
    KeyValuePair(K k, V v) : key(k), value(v) {}
};


template <typename K, typename V, int SIZE>
class ArrayMap {
private:
    KeyValuePair<K, V> pairs[SIZE];
    int size;

public:
    template <typename... Args>
    ArrayMap(Args... args) : size(0) {
        KeyValuePair<K, V> initPairs[SIZE] = { KeyValuePair<K, V>(args)... };

        for (int i = 0; i < SIZE; ++i) {
            insert(initPairs[i].key, initPairs[i].value);
        }
    }
    void insert(K key, V value) {
        if (size < SIZE) {
            pairs[size++] = KeyValuePair<K, V>(key, value);
        }
    }
    V* search(K key) {
        for (int i = 0; i < size; ++i) {
            if (pairs[i].key == key) {
                return &pairs[i].value;
            }
        }
        return nullptr;
    }

};