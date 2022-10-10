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
    PointSet((*this)*(other.transpose())) a;
    JacobiSVD<Matrix3f, ComputeThinU | ComputeThinV> svd(a);
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