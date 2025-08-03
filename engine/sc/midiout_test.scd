s.reboot;
MIDIClient.init;
MIDIClient.destinations;
MIDIClient.externalSources;

~midiPort = MIDIClient.destinations.detectIndex{|src| src.device.contains("USB")}
~midiOut = MIDIOut(~midiPort, MIDIClient.destinations[~midiPort].uid);
~midiOut.start;
~midiOut.midiClock
~midiOut.stop;
MIDIClient.destinations[1].uid

// Set tempo (BPM)
~tempo = 120; // BPM
~clock = TempoClock(~tempo / 60); // Convert to beats/sec

// Start/stop the MIDI clock
~midiClockRoutine = nil;

~startMidiClock = {
    if (~midiClockRoutine.notNil) { ~midiClockRoutine.stop };
    ~midiOut.start; // Send MIDI Start
    ~midiClockRoutine = {
        loop {
            ~midiOut.midiClock; // Send tick
            (1/24).wait; // Wait for 1/24th of a beat
        }
    }.fork(~clock, quant: 0); // Start immediately
};

~stopMidiClock = {
    ~midiClockRoutine.stop;
    ~midiClockRoutine = nil;
    ~midiOut.stop; // Send MIDI Stop
};

~continueMidiClock = {
    if (~midiClockRoutine.notNil) { ~midiClockRoutine.stop };
    ~midiOut.continue; // Send MIDI Continue
    ~midiClockRoutine = {
        loop {
            ~midiOut.clock;
            (1/24).wait;
        }
    }.fork(~clock, quant: 0);
};

~startMidiClock.();

~stopMidiClock.();