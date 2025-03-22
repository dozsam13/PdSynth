s.boot;
~bs = SoundFile.collectIntoBuffers("C:/dev/PdSynth/samples/emx-sample-pack-50tube/*");


(
SynthDef.new(\sampy, {
	var sig, env;

	sig = PlayBuf.ar(
		numChannels: 2,
		bufnum: \buf.kr(0),
		rate: BufRateScale.kr(\buf.kr(0)) * \rate.kr(1),  //44100/44100
		startPos: \spos.kr(0)
	);
	env = EnvGen.kr(
		envelope: Env(
			levels: [0, 1, 0],
			times:[\atk.ir(0.01), \decay.ir(0.5)],
			curve: [0, 0]
		),
		doneAction: 2
	);
	Out.ar(\out.kr(0), sig*env*\amp.kr(1));
}).add;
)

s.plotTree;
a = Synth(\sampy, [\buf, ~bs[14].bufnum, \rate, 1]);

(
t = TempoClock.new(200/60).permanent_(true);
~postBeat = {t.beats.postln;1;};
t.schedAbs(t.nextBar, {~postBear.value});
)

(
~amp1 = 1;
~p1 = Pbind(
	\instrument, \sampy,
	\buf, ~bs[14].bufnum,
	\rate, Pseq([1, 1.5, 1, 1, 1, 1, 1, 1], inf),
	\freq, Pseq([100, 100], inf),
	\amp, Pfunc({~amp1})
);
)
~amp1 = 0.5;
(
~player = ~p1.play(t, quant:2);
)
~player.stop;