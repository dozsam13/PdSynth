s.boot;
MIDIClient.init;
MIDIIn.connect(0, MIDIClient.sources.detectIndex{|src| src.device.contains("USB")});
//Quarks.install("ddwMIDI");

//Quarks.gui;
//Quarks.install("https://github.com/supercollider-quarks/MidiSyncClock");

MIDISyncClock.init;

MIDISyncClock.tempo;
(
~myPattern = Pbind(
    \intrument, \default,
    \dur, 1,
    \amp, 1
).play(MIDISyncClock, quant:4);
)

t = TempoClock.new(200/60).permanent_(true);
//p = Pbind(\degree, Pn(Pseries(0,1,8),inf), \dur, 0.5).play(t);

~bs = SoundFile.collectIntoBuffers("/home/jozef1957/dev/PdSynth/samples/emx-sample-pack-50tube/*");
(
SynthDef.new(\play, {
	var sig, env;

	sig = PlayBuf.ar(
		numChannels: 1,
		bufnum: \buf.kr(0),
		rate: BufRateScale.kr(\buf.kr(0)) * \rate.kr(1),
		startPos: \spos.kr(0),
		loop: \loop.ir(0)
	);

	sig = LPF.ar(sig, \lpf.ir(20000).clip(20, 20000));
	sig = HPF.ar(sig, \hpf.ir(20).clip(20, 20000));

	env = EnvGen.kr(
		Env(
			levels: [0, 1, 0],
			times: [\atk.ir(0.02), \rel.ir(3)],
			curve: [-2, -4],
		),
		doneAction: 2
	);

	sig = Pan2.ar(sig, \pan.kr(0));
	sig = sig * env;
	sig = sig * \amp.kr(1);

	Out.ar(\out.kr(0), sig);
}).add;
)

(
r = Routine.new({
	Synth.new(\play, [buf: ~bs[0], rate: -7.midiratio]);
	0.25.wait;
	Synth.new(\play, [buf: ~bs[0], rate: -5.midiratio]);
	0.25.wait;
	Synth.new(\play, [buf: ~bs[0], rate: 2.midiratio]);
	0.25.wait;
});
)
r.play;