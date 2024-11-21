struct tuple_t {
    unsigned int key;
    float value;
    float aggregate;
    unsigned int timestamp;

    tuple_t() = default;

    tuple_t(unsigned int key, float value, float aggregate, unsigned int timestamp)
        : key(key), value(value), aggregate(aggregate), timestamp(timestamp)
    {}

    #if !defined(SYNTHESIS)
    friend std::ostream & operator<<(std::ostream & os, const tuple_t & d)
    {
        os << "(key: " << d.key << ", value: " << d.value << ", aggregate: " << d.aggregate << ", timestamp: " << d.timestamp << ")";
        return os;
    }
    #endif
};

auto tuple_key_extractor = [](const tuple_t & t) { return t.key; };

struct result_t
{
    float sum;
    unsigned int count;

    result_t()
    : sum(0)
    , count(0)
    {}

    float mean() const {
        return sum / count;
    }

    #if !defined(__SYNTHESIS__)
    friend std::ostream & operator<<(std::ostream & os, const result_t & d)
    {
        os << "(sum: " << d.sum << ", count: " << d.count << ")";
        return os;
    }
    #endif
};

struct window_functor
{
    void operator()(const tuple_t & tuple, result_t & result)
    {
    #pragma HLS INLINE
        result.sum += tuple.value;
        result.count = result.count + 1;
    }
};
