s.boot;
s.reboot;
s.freeAll;
s.doWhenBooted({
Platform.userExtensionDir;
~bs = SoundFile.collectIntoBuffers("/home/jozef1957/dev/PdSynth/samples/emx-sample-pack-50tube/*");
~bs[0].path.postln;

(
(
SynthDef.new(\sampy, {
	var sig, env, envgen, sig2;

	sig = PlayBuf.ar(
		numChannels: 2,
		bufnum: \buf.kr(0),
		rate: BufRateScale.kr(\buf.kr(0)) * \rate.kr(1),  //44100/44100
		startPos: \spos.kr(0)
	);
	/*env = Env.new(
		levels: [0, 1, 1, 0], // levels
		times: [\attack.kr(0.01), \sustain.kr(1.0), \release.kr(0.1)],
		curve: 'lin'
	).kr(doneAction: 2);*/

	env = EnvGen.ar(
		Env.perc(attackTime: \attack.kr(0.01), releaseTime: \release.kr(0.1), level: 1.0, curve: -1.0),
		doneAction: 2
	);
	//sig = GlitchBPF..ar(in: sig, freq: 440.0, rq: 1.0, mul: 1.0, add: 0.0);
				sig = CrossoverDistortion.ar(sig, amp: \distortion_amp.kr(0.5), smooth: \distortion_smooth.kr(0.5), mul: 1.0, add: 0);
	sig = RLPF.ar(in: sig, freq: \cutoff.kr(2200.0), rq: \resonance.kr(0.01), mul: 1.0, add: 0.0);
	Out.ar(\out.kr(0), env*sig*\amp.kr(1)*\mute.kr(1));
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

	~paramDict.put(("amp_" ++ track_id).asSymbol, 0.0);
	~paramDict.put(("bufnum_" ++ track_id).asSymbol, ~bs[14].bufnum);
	~paramDict.put(("rate_" ++ track_id).asSymbol, Pseq([1.0], 1));
	~paramDict.put(("mute_" ++ track_id).asSymbol, 1.0);
	~paramDict.put(("freq_" ++ track_id).asSymbol, Pseq([100, \, \, \], 1));
	//AMP
	~paramDict.put(("attack_" ++ track_id).asSymbol, 0.001);
	~paramDict.put(("sustain_" ++ track_id).asSymbol, 1.0);
	~paramDict.put(("release_" ++ track_id).asSymbol, 0.5);
	//FILTER
	~paramDict.put(("cutoff_" ++ track_id).asSymbol, 2200.0);
	~paramDict.put(("resonance_" ++ track_id).asSymbol, 0.1);
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

	OSCdef(("sustain_" ++ track_id).asSymbol, { |msg|
		~paramDict[("sustain_" ++ track_id).asSymbol] = msg[1];
	}, "/sustain_" ++ track_id);

	OSCdef(("release_" ++ track_id).asSymbol, { |msg|
		~paramDict[("release_" ++ track_id).asSymbol] = msg[1];
	}, "/release_" ++ track_id);

	OSCdef(("cutoff_" ++ track_id).asSymbol, { |msg|
		~paramDict[("cutoff_" ++ track_id).asSymbol] = msg[1];
	}, "/cutoff_" ++ track_id);

	OSCdef(("resonance_" ++ track_id).asSymbol, { |msg|
		~paramDict[("resonance_" ++ track_id).asSymbol] = msg[1];
	}, "/resonance_" ++ track_id);

	OSCdef(("mute_" ++ track_id).asSymbol, { |msg|
		~paramDict[("mute_" ++ track_id).asSymbol] = msg[1];
	}, "/mute_" ++ track_id);

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
		\mute, Pfunc({~paramDict[("mute_" ++ track_id).asSymbol]}),
		\freq, Pn(Plazy({~paramDict[("freq_" ++ track_id).asSymbol]}), inf),
		//amp
		\attack, Pfunc({~paramDict[("attack_" ++ track_id).asSymbol]}),
		\sustain_, Pfunc({~paramDict[("sustain_" ++ track_id).asSymbol]}),
		\release, Pfunc({~paramDict[("release_" ++ track_id).asSymbol]}),
		//filter
		\cutoff, Pfunc({~paramDict[("cutoff_" ++ track_id).asSymbol]}),
		\resonance, Pfunc({~paramDict[("resonance_" ++ track_id).asSymbol]})
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
})


~players = ~patterns.collect({ |ptn| ptn.play(t)});

~players.do({ |player| player.stop;});

~paramDict[("amp_1").asSymbol] = 1;
~paramDict[("amp_2").asSymbol] = 0;

~paramDict[("bufnum_1").asSymbol] = 1;
~paramDict[("attack_1").asSymbol] = 0.05;
~paramDict[("bufnum_2").asSymbol] = msg[1];

~paramDict[("attack_1").asSymbol] = 0.0;
~paramDict[("sustain_1").asSymbol] = 1.5;
~paramDict[("release_1").asSymbol] = 1.0;
s.freeAll;
s.queryAllNodes;
