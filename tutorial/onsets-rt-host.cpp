#include "onsets.cpp"

#include <iostream>
#include <mutex>
#include <condition_variable>
#include <memory>
#include <thread>
#include <RtAudio.h>

using namespace std;

class Buffer
{
public:
    Buffer(int capacity):
        data(capacity)
    {}

    void write(double * d, int count)
    {
        lock_guard<std::mutex> lock(mutex);

        for (int i = 0; i < count; ++i)
        {
            data[writePos] = d[i];
            ++writePos;
            if (!shiftIfFull())
            {
                cerr << "Buffer overrun." << endl;
                break;
            }
        }

        signal.notify_all();
    }

    void read(double * d, int count)
    {
        unique_lock<std::mutex> lock(mutex);

        while(writePos - readPos < count)
        {
            signal.wait(lock);
        }

        for (int i = 0; i < count; ++i)
        {
            d[i] = data[readPos];
            ++readPos;
        }
    }

private:
    bool shiftIfFull()
    {
        if (writePos != capacity())
            return true;

        int moveCount = capacity() - readPos;

        if (moveCount <= 0)
            return false;

        for (int i = 0; i < moveCount; ++i)
        {
            data[i] = data[i+readPos];
        }

        readPos = 0;
        writePos = readPos + moveCount;

        return true;
    }

    int capacity() const { return int(data.size()); }

    std::mutex mutex;
    std::condition_variable signal;
    vector<double> data;
    int readPos = 0;
    int writePos = 0;
};

Buffer g_buffer(44100);

struct IO
{
    void input_x(double & data)
    {
        g_buffer.read(&data, 1);
    }

    void output_y(bool value)
    {
        cout << value << endl;
    }
};

int process( void *outputBuffer, void *inputBuffer, unsigned int nBufferFrames,
             double streamTime, RtAudioStreamStatus status, void *userData )
{
  if ( status )
    cerr << "Stream overflow detected!" << endl;

  g_buffer.write((double*)inputBuffer, nBufferFrames);

  return 0;
}

void process()
{
    IO io;

    auto program = make_shared<m::program<IO>>();
    program->io = &io;

    program->prelude();

    while(true)
    {
        program->period();
    }
}

int main()
{
  RtAudio adc;
  if ( adc.getDeviceCount() < 1 ) {
    std::cout << "\nNo audio devices found!\n";
    exit( 0 );
  }

  RtAudio::StreamParameters parameters;
  parameters.deviceId = adc.getDefaultInputDevice();
  parameters.nChannels = 1;
  parameters.firstChannel = 0;
  unsigned int sampleRate = 44100;
  unsigned int bufferFrames = 512;
  try {
    adc.openStream( NULL, &parameters, RTAUDIO_FLOAT64,
                    sampleRate, &bufferFrames, &process );
    adc.startStream();
  }
  catch ( RtAudioError& e ) {
    e.printMessage();
    exit( 0 );
  }

  if (parameters.nChannels != 1)
  {
      cerr << "Could not start stream with 1 channel.\n";
  }
  else
  {
      process();
  }

  try {
    // Stop the stream
    adc.stopStream();
  }
  catch (RtAudioError& e) {
    e.printMessage();
  }
  if ( adc.isStreamOpen() ) adc.closeStream();
  return 0;
}

