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

(
t = TempoClock.new(200/60).permanent_(true);
~postBeat = {t.beats.postln;1;};
t.schedAbs(t.nextBar, {~postBear.value});
)

(
~paramDict = Dictionary();
~patterns = [];
~paramDict.put(\amp_1, 1.0);
~paramDict.put(\bufnum_1, ~bs[14].bufnum);
~paramDict.put(\rate_1, Pseq([1.0], 1));
~paramDict.put(\freq_1, Pseq([100, \, \, \], 1));

~paramDict.put(\amp_2, 1.0);
~paramDict.put(\bufnum_2, ~bs[63].bufnum);
~paramDict.put(\rate_2, Pseq([1.0], 1));
~paramDict.put(\freq_2, Pseq([\, \, 100, \], 1));
)

(
~patterns = [1,2].collect{
	arg track_id;

	// Create OSC param bindings
	OSCdef(("amp_" ++ track_id).asSymbol, { |msg|
		//msg[1].postln;
		~paramDict[("amp_" ++ track_id).asSymbol] = msg[1];
	}, "/amp_" ++ track_id);

	OSCdef(("bufnum_" ++ track_id).asSymbol, { |msg|
		//msg[1].postln;
		~paramDict[("bufnum_" ++ track_id).asSymbol] = msg[1];
	}, "/bufnum_" ++ track_id);

	OSCdef(("rate_" ++ track_id).asSymbol, { |msg|
		//msg[1].postln;
		~paramDict[("rate_" ++ track_id).asSymbol] = Pseq([msg[1]], 1);
	}, "/rate_" ++ track_id);

	OSCdef(("freq_" ++ track_id).asSymbol, { |msg|
		var seq, s2;
		seq = msg.drop(1);
		s2 = seq.collect({ |m2|
			if(m2 == 0) {
				0;
			}{
				"\\";
			}
		});
		s2.postln;
		("freq" ++ track_id).asSymbol.postln;
		~paramDict[("freq" ++ track_id).asSymbol] = Pseq(s2, 1);
	}, "/freq_" ++ track_id);


	// Create Pattern for track
	Pbind(
		\instrument, \sampy,
		\dur, 0.25,
		\amp, Pfunc({~paramDict[("amp_" ++ track_id).asSymbol]}),
		\buf, Pfunc({~paramDict[("bufnum_" ++ track_id).asSymbol]}),
		\rate, Pn(Plazy({~paramDict[("rate_" ++ track_id).asSymbol]}), inf),
		\freq, Pn(Plazy({~paramDict[("freq_" ++ track_id).asSymbol]}), inf)
	);

}
)

(
OSCdef(\start_seq, { |msg|
	~players = ~patterns.collect({ |ptn|
		ptn.play(t)
	});

}, "/start_seq");

OSCdef(\stop_seq, { |msg|
	~players.do({ |player|
		player.stop;
	});
}, "/stop_seq");
)
(
~plr1 = ~patterns[0].play(t);
~plr2 = ~patterns[1].play(t);
)

~paramDict[\amp_1] = 1.0;
~paramDict[\amp_2] = 0.7;
~paramDict[\rate_1] = Pseq([1.0], 1);
~paramDict[\rate_2] = Pseq([1.0], 1);
~paramDict[\freq_1] = Pseq([0, \, \, \], 1);
~patterns.size.postln;

(
~plr1.stop;
~plr2.stop;
)
s.freeAll;
