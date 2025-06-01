s.boot;
s.reboot;
s.freeAll;
//s.doWhenBooted({
~bs = SoundFile.collectIntoBuffers("C:\\dev\\PdSynth\\samples\\emx-sample-pack-50tube\\*");
~bs[0].path.postln;

(
(
SynthDef.new(\sampy, {
	var sig, env, envgen;

	sig = PlayBuf.ar(
		numChannels: 2,
		bufnum: \buf.kr(0),
		rate: BufRateScale.kr(\buf.kr(0)) * \rate.kr(1),  //44100/44100
		startPos: \spos.kr(0)
	);
	env = Env.new(
		levels: [0, 1, \sustain_level.kr(1.0), 0], // levels
		times: [\attack.kr(0.01), \decay.kr(0.3), \release.kr(0.1)],
		curve: 'lin'
	).kr(doneAction: 2);


	Out.ar(\out.kr(0), sig*env*\amp.kr(1));
}).add;
);

(
t = TempoClock.new(200/60).permanent_(true);
~postBeat = {t.beats.postln;1;};
t.schedAbs(t.nextBar, {~postBear.value});
);

(
~track_ids = [1, 2];
~paramDict = Dictionary();
~patterns = [];
~track_ids.do({
	arg track_id;

	~paramDict.put(("amp_" ++ track_id).asSymbol, 1.0);
	~paramDict.put(("bufnum_" ++ track_id).asSymbol, ~bs[14].bufnum);
	~paramDict.put(("rate_" ++ track_id).asSymbol, Pseq([1.0], 1));
	~paramDict.put(("freq_" ++ track_id).asSymbol, Pseq([100, \, \, \], 1));
	//AMP
	~paramDict.put(("attack_" ++ track_id).asSymbol, 0.001);
	~paramDict.put(("decay_" ++ track_id).asSymbol, 1.0);
	~paramDict.put(("sustain_level" ++ track_id).asSymbol, 1.0);
	~paramDict.put(("release_" ++ track_id).asSymbol, 0.5);
});
);
(
~patterns = ~track_ids.collect{
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

	OSCdef(("attack_" ++ track_id).asSymbol, { |msg|
		~paramDict[("attack_" ++ track_id).asSymbol] = msg[1];
	}, "/attack_" ++ track_id);

	OSCdef(("decay_" ++ track_id).asSymbol, { |msg|
		~paramDict[("decay_" ++ track_id).asSymbol] = msg[1];
	}, "/decay_" ++ track_id);

	OSCdef(("sustain_" ++ track_id).asSymbol, { |msg|
		~paramDict[("sustain_" ++ track_id).asSymbol] = msg[1];
	}, "/sustain_" ++ track_id);

	OSCdef(("release_" ++ track_id).asSymbol, { |msg|
		~paramDict[("release_" ++ track_id).asSymbol] = msg[1];
	}, "/release_" ++ track_id);

	OSCdef(("sustain_level_" ++ track_id).asSymbol, { |msg|
		~paramDict[("sustain_level_" ++ track_id).asSymbol] = msg[1];
	}, "/sustain_level_" ++ track_id);

	OSCdef(("freq_" ++ track_id).asSymbol, { |msg|
		var seq, s2;
		seq = msg.drop(1);
		seq.postln;
		~paramDict[("freq_" ++ track_id).asSymbol] = Pseq(seq, 1);
	}, "/freq_" ++ track_id);


	// Create Pattern for track
	Pbind(
		\instrument, \sampy,
		\dur, 0.25,
		\amp, Pfunc({~paramDict[("amp_" ++ track_id).asSymbol]}),
		\buf, Pfunc({~paramDict[("bufnum_" ++ track_id).asSymbol]}),
		\rate, Pn(Plazy({~paramDict[("rate_" ++ track_id).asSymbol]}), inf),
		\freq, Pn(Plazy({~paramDict[("freq_" ++ track_id).asSymbol]}), inf),
		//amp
		\attack, Pfunc({~paramDict[("attack_" ++ track_id).asSymbol]}),
		\decay, Pfunc({~paramDict[("decay_" ++ track_id).asSymbol]}),
		\sustain_level, Pfunc({~paramDict[("sustain_level" ++ track_id).asSymbol]}),
		\release, Pfunc({~paramDict[("release_" ++ track_id).asSymbol]}),
	);

});

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

OSCdef(\bpm, { |msg|
	t.tempo = msg[1]/60;
}, "/bpm");

OSCdef(\volume, { |msg|
	s.volume.volume = if(msg[1] > 1) {1} {msg[1]};
}, "/volume");
);

)
//})

~players = ~patterns.collect({ |ptn| ptn.play(t)});
~players.do({ |player| player.stop;});
~paramDict[("amp_1").asSymbol] = 1;
~paramDict[("amp_2").asSymbol] = 0;

~paramDict[("bufnum_1").asSymbol] = 10;
~paramDict[("attack_1").asSymbol] = 0.05;
~paramDict[("bufnum_2").asSymbol] = msg[1];
s.freeAll;
s.queryAllNodes;