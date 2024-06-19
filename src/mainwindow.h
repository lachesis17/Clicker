#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QTextEdit>
#include <QGraphicsColorizeEffect>
#include <QPropertyAnimation>
#include <QParallelAnimationGroup>
#include <vector>
#include <string>
#include "src/clicker.h"
#include "src/threadHandler.h"
using namespace std;

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    Clicker* clicker = new Clicker();
    ThreadHandler* worker = new ThreadHandler();
private:
    Ui::MainWindow *ui;
    QPushButton *click_button;
    QTextEdit *text_edit;
public slots:
    void handleClick();
    void updateDisplay(vector<string> values);
};
#endif // MAINWINDOW_H