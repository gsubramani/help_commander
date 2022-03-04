#include<cstdint>
#include<cstring>
#include<cstdlib>
#include<iostream>
#include<climits>

typedef float           F32 ; static_assert(sizeof(F32)  == 4 , "TYPE SIZE ERROR");
typedef uint8_t         BYTE; static_assert(sizeof(BYTE) == 1 , "TYPE SIZE ERROR");




struct alignas(F32) Parameters {

    F32 k1;
    F32 ks[2];

} parameters;


static_assert(sizeof(uint64_t) == sizeof(uintptr_t) , "TYPE SIZE ERROR");



struct StructLookup 
{

    uint64_t       location_offset;
    uint32_t       size;
    void*          data;

    StructLookup(const void* struct_ptr, const void* member_ptr, const uint32_t _size) : size(_size)
    {
        data = malloc(_size);
        memcpy( data, member_ptr, _size);
        location_offset = (   reinterpret_cast<uint64_t>(member_ptr) 
                            - reinterpret_cast<uint64_t>(struct_ptr)
                         ); 
    }

    StructLookup(uint64_t _location_offset, uint32_t _size, void* _data) : location_offset(_location_offset) ,size(_size) 
    {
        data = malloc(_size);
        memcpy(data, _data, size);

    }

    void PushData(void* struct_ptr)
    {
        memcpy( reinterpret_cast<void*> (reinterpret_cast<uintptr_t>(struct_ptr) + location_offset), data, size); 
    }

    ~StructLookup()
    {
        free(data);
    }

};

uint32_t wrapped_diff(uint32_t smaller, uint32_t larger)
{
    return (larger >= smaller) ? 
                              (larger - smaller) 
                            : ((UINT_MAX - smaller) +  larger + 1);  
}



int main()
{

    Parameters params_in, params_out;
    params_in.k1 = 3.3f;
    params_in.ks[0] = 1.0f;
    params_in.ks[1] = 2.0f;


    params_out.k1       = 0.0f;
    params_out.ks[0]    = 0.0f;
    params_out.ks[1]    = 0.0f;


    StructLookup(&params_in, &params_in.k1, sizeof(params_in.k1)).PushData(&params_out);


    std::cout << params_out.k1 <<std::endl;
    std::cout << params_out.ks[0] <<std::endl;
    std::cout << params_out.ks[1] <<std::endl;

    std::cout << wrapped_diff(UINT32_MAX - 10, 2u ) << std::endl;
    std::cout << wrapped_diff(2u, 100u) << std::endl;
    std::cout << wrapped_diff(0, UINT32_MAX) << std::endl;
    std::cout << wrapped_diff(UINT32_MAX, UINT32_MAX) << std::endl;
    std::cout << wrapped_diff(UINT32_MAX, 0) << std::endl;
    std::cout << wrapped_diff(UINT32_MAX + 1, 0) << std::endl;
    


}