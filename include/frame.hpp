#ifndef _FRAME_HPP_
#define _FRAME_HPP_

#include<Eigen/Dense>

using namespace Eigen;
class Frame {
    public:
    Matrix3f R;
    Vector3d p;

    Frame(Matrix3f R, Vector3d p) {
        R = R;
        p = p;
    }

    Frame composeFrame(Frame other) {
        Vector3d vec = this->R*other.p;
        vec+=this->p;
        Matrix3f mat = this->R*other.R;
        return Frame(mat, vec);
    }

    Vector3d composeVec(Vector3d v){
        Vector3d vec = this->R*v;
        vec+=this->p;
        return vec;
    }

    Frame invert() {
        Matrix3f mat;
        if(this->R.determinant() != 0) {
            mat = this->R.inverse();
        } 
        // else do smtg to matrix to make it invertible
        Vector3d vec = mat*this->p;
        vec*= -1;
        return Frame(mat, vec);
    }
}


#endif