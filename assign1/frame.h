#ifndef FRAME_H_
#define FRAME_H_

#include <linalg.h>

class Frame {
    public:
    
    linalg::mat<double, 3, 3> R;
    linalg::vec<double, 3> p;

    Frame(linalg::mat<double, 3, 3> rot, linalg::vec<double, 3> trans) {
        R = rot;
        p = trans;
    }

    Frame composeFrame(Frame other);
    
    linalg::vec<double, 3> composeVec(linalg::vec<double, 3> v);

    Frame invert();


}



#endif
