#ifndef _FRAME_HPP_
#define _FRAME_HPP_

#include<Eigen/Dense>
#include "frame.hpp"

using namespace Eigen;
class PointSet() {

public:
Matrix3f points;

PointSet(MatrixXf p) {
    points = p;
}

Frame registration(PointSet other) {
    //callibrate center of gravity somehow?
    //do smtg w the means
    VectorXf meanA;
    meanA.resize(this->rows());
    for(int i = 0; i < this->rows(); i++){
        float m = 0;
        for(int j = 0; j < this->cols(); j++){
            m+= (*this)(row, col);
        }
        meanA(i) = m/(this->cols());
    }

    VectorXf meanB;
    meanB.resize(other.rows());
    for(int i = 0; i < other.rows(); i++){
        float m = 0;
        for(int j = 0; j < other.cols(); j++){
            m+= other(row, col);
        }
        meanB(i) = m/(other.cols());
    }

    MatrixXf centeredA = *this - meanA;
    MatrixXf centeredB = other - meanB;
    
    PointSet((other)*(*this.transpose())) BAt;
    JacobiSVD<Matrix3f, ComputeThinU | ComputeThinV> svd(BAt);
    PointSet(svd.matrixU()) U;
    U = U.transpose();
    Matrix3f s = svd.singularValues().asDiagonal();
    Matrix3f R = S*(svd.mattrixV().transform);
    R = U*R;
    //this isn't entirely correct
    //have to account for error
}



}

#endif