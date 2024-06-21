#include "src/mainwindow.h"
#include "clicker.h"
#include <iostream>
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    //a.setAttribute(Qt::AA_UseHighDpiPixmaps, true);
    MainWindow w;
    w.show();
    return a.exec();
}