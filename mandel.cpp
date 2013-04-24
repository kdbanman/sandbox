#include <stdio.h>
#include <pthread.h>
#include <complex>
#include <assert.h>

////////////////////////////////////////

class Screen
{
private:
  int W, H, size;

  bool *pixel;

public:
  Screen(int w, int h);
  ~Screen();
};

Screen::Screen(int w, int h)
{
  W = w;
  H = h;
  size = W*H;
  pixel = new bool(size);
}

Screen::~Screen()
{
  delete pixel;
}

////////////////////////////////////////

class MandelbrotInterval
{
private:
  complex<double> MIN(-2, -1);
  complex<double> MAX(1,1);

  complex<double> lower, upper, MIN, MAX;

  double division;

public:
  MandelbrotInterval(int w, int h);
  ~MandelbrotInterval();
  
  setDivision(double d);
  setBounds(complex<double> l, complex<double> h);
}

////////////////////////////////////////

bool converges(complex<double> c, int N)
{
  int i = 0;
  complex<double> z(0,0);
  while (abs(z) < 2 && i < N) {
    z = z*z + c;
    i++;
  }
}

int main()
{
  

  return 0;
}
