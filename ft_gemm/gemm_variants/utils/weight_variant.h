

enum WeightVariant { kFP16, kBF16, kFP8, kFP4};

template <WeightVariant V>
class WeightStorageType;

template <>
class WeightStorageType<WeightVariant::kFP16> {
public:
    using type = half;
};

template <>
class WeightStorageType<WeightVariant::kBF16> {
public:
    using type = nv_bfloat16;
};

template <>
class WeightStorageType<WeightVariant::kFP8> {
public:
    using type = uint8_t;
};

template <>
class WeightStorageType<WeightVariant::kFP4> {
    public:
    using type = cutlass::uint4b_t;
};
