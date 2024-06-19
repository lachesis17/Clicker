#include "src/mainwindow.h"
#include "src/clicker.h"
#include "../assets/ui_main_window.h"
#include <QCoreApplication>
#include <QMetaType>
#include <iostream>
#include <vector>
#include <string>
using namespace std;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    qRegisterMetaType<std::vector<std::string>>("std::vector<std::string>");

    ui->setupUi(this);
    setWindowIcon(QIcon("mouse.ico")); 
    setWindowTitle("Clicker");
    ui->click_button->setIcon(QIcon("mouse.svg"));
    connect(ui->click_button, &QPushButton::released, this, &MainWindow::handleClick);

    worker->setFunction([this]() {
        clicker->click_me();
    });

    QObject::connect(clicker, &Clicker::updateText, this, &updateDisplay);

}

void MainWindow::handleClick() {
    ui->text_edit->clear();
    if (ui->click_button->isChecked())
        {
            clicker->keepRunning = true;
            if (!worker->isRunning())
                worker->start();
        }
    else
        {
            clicker->keepRunning = false;
            worker->quit();
            std::vector<std::string> stop = {"❌"};
            updateDisplay(stop);
        }
    };

void MainWindow::updateDisplay(vector<string> values) {
    ui->text_edit->clear();
    std::vector<std::string> colors = {"red", "green", "blue", "purple", "orange", "cyan", "magenta", "lime", "pink"};
    int colorIndex = clicker->counter;

    for(auto& item : values)
    {
        std::string color = colors[colorIndex % colors.size()];
        ui->text_edit->setTextColor(QColor(QString::fromStdString(color)));
        ui->text_edit->setFontWeight(QFont::Bold);
        ui->text_edit->setAlignment(Qt::AlignCenter);
        ui->text_edit->append(QString::fromStdString(item));
        colorIndex++;
    }
}

MainWindow::~MainWindow()
{
    delete ui;
}
