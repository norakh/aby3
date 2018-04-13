#pragma once
#include "Sh3Defines.h"

#include "aby3/Circuit/BetaCircuit.h"
#include "Sh3Runtime.h"
#include <cryptoTools/Crypto/sha1.h>

namespace aby3
{

	class Sh3BinaryEvaluator
	{
	public:

#define BINARY_ENGINE_DEBUG
#ifdef BINARY_ENGINE_DEBUG
    private:
        bool mDebug = false;
    public:

        void enableDebug(u64 partyIdx, oc::Channel debugPrev, oc::Channel debugNext)
        {
            mDebug = true;
            mDebugPartyIdx = partyIdx;

            mDebugPrev = debugPrev;
            mDebugNext = debugNext;
        }

		struct DEBUG_Triple
		{
			std::array<u8, 3> mBits;
            bool mIsSet;
			u16 val()const { return mBits[0] ^ mBits[1] ^ mBits[2]; }

			void assign(const DEBUG_Triple& in0, const DEBUG_Triple& in1, oc::GateType type);
		};
		std::vector<std::vector<DEBUG_Triple>> mPlainWires_DEBUG;
        u64 mDebugPartyIdx=-1;
        oc::Channel mDebugPrev, mDebugNext;

        u8 extractBitShare(u64 rowIdx, u64 wireIdx, u64 shareIdx);

        void validateMemory();
        void validateWire(u64 wireIdx);
#endif

        oc::BetaCircuit* mCir;
        oc::BetaGate* mGateIter;
		u64 mLevel;
		std::vector<u32> mRecvLocs;
        std::vector<i64> mRecvData;
        std::future<void> mRecvFutr;
        Sh3::sPackedBin mMem;

        
        void setCir(oc::BetaCircuit* cir, u64 width);

        void setReplicatedInput(u64 i, const Sh3::sbMatrix& in);
        void setInput(u64 i, const Sh3::sbMatrix& in);
        void setInput(u64 i, const Sh3::sPackedBin& in);

        Sh3Task asyncEvaluate(Sh3Task dependency, oc::BetaCircuit* cir, std::vector<const Sh3::sbMatrix*> inputs, std::vector<Sh3::sbMatrix*> outputs);
        Sh3Task asyncEvaluate(Sh3Task dependency);
        
        
        void roundCallback(Sh3::CommPkg& comms, Sh3Task task);

        void getOutput(u64 i, Sh3::sbMatrix& out);
        void getOutput(u64 i, Sh3::sPackedBin& out);
		void getOutput(const std::vector<oc::BetaWire>& wires, Sh3::sbMatrix& out);

		bool hasMoreRounds() const {
			return mLevel <= mCir->mLevelCounts.size();
		}


        oc::block hashState()
        {
            oc::SHA1 h(sizeof(block));
            h.Update(mMem.mShares[0].data(), mMem.mShares[0].size());
            h.Update(mMem.mShares[1].data(), mMem.mShares[1].size());

            block b;
            h.Final(b);
            return b;
        }
	};

}