#ifndef THREADHANDLER_H
#define THREADHANDLER_H

#include <QThread>
#include <iostream>

class ThreadHandler : public QThread {
public:
    std::function<void()> func;

    void setFunction(const std::function<void()>& f)
    {
        func = f;
    }

protected:
    void run() override
    {
        if (func)
        {
            func();
        }
    }
};

#endif // THREADHANDLER_H
