#include "frame.h"

using namespace linalg::aliases;

Frame composeFrame(Frame other){
    double3 vec = mul(this->R, other.p);
    vec+=this->p;
    double3X3 mat = mul(this->R, other.R);
    return Frame(mat, vec)
}

double3 composeVec(linalg::vec<double, 3> v){
    double3 vec = mul(this->R, v);
    vec+=this->p;
    return vec;
}

Frame invert(){
    double 3x3 mat;
    if(determinant(this->R) != 0) {
        mat = inverse(this->R);
    } 
    // else do smtg to matrix to make it invertible
    double3 vec = mul(mat, this->p);
    vec*= -1;
    return Frame(mat, vec);
}
