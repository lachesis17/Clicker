#pragma once
#include <windows.h>
#include <QWidget>
#include <vector>
#include <string>

class Clicker : public QWidget
{
    Q_OBJECT  // Required for any class that defines signals or slots despite QWidget inheriting from QObject
public:
    Clicker() {}
    ~Clicker() {}

    bool keepRunning = false;
    int counter = 0;

    void click_me()
    {
        counter = 0;
        std::vector<std::string> history = {"🐭"};
        emit updateText(history);
        std::vector<std::string> colors = {"red", "green", "blue", "purple", "orange", "cyan", "magenta", "lime", "pink"};

        while (keepRunning)
        {
            Sleep(3000);
            leftClick();
            counter++;
            history.push_back(std::to_string(counter));
            if (keepRunning)
            {
                size_t numElements = 10;
                if (history.size() > numElements)
                    {
                        std::vector<std::string> slice;
                        slice.reserve(numElements);
                        std::copy(history.end() - numElements, history.end(), std::back_inserter(slice));
                        emit updateText(slice);
                    }
                else
                    {
                        emit updateText(history); 
                    }
            }
        }

        emit updateText({"🌈"});
    }

    void leftClick()
    {
        INPUT input = {0};                          // Structure for the mouse event

        input.type = INPUT_MOUSE;
        input.mi.dx = 0;                            // X coordinate, not needed for click itself
        input.mi.dy = 0;                            // Y coordinate, not needed for click itself
        input.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;    // Mouse event left button down
        SendInput(1, &input, sizeof(INPUT));        // Send the mouse event down

        ZeroMemory(&input, sizeof(INPUT));
        input.type = INPUT_MOUSE;
        input.mi.dx = 0;
        input.mi.dy = 0;
        input.mi.dwFlags = MOUSEEVENTF_LEFTUP;      // Mouse left button up
        SendInput(1, &input, sizeof(INPUT));        // Send the mouse event up
    }

signals:
    void updateText(const std::vector<std::string>& text);
};